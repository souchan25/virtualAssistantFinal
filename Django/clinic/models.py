"""
Core models for CPSU Virtual Health Assistant
Includes custom user model, health records, and audit logs
"""

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class CustomUserManager(BaseUserManager):
    """Manager for custom user model"""
    
    def create_user(self, school_id, password=None, **extra_fields):
        """Create and save a regular user"""
        if not school_id:
            raise ValueError('School ID is required')
        
        user = self.model(school_id=school_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, school_id, password=None, **extra_fields):
        """Create and save a superuser"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'staff')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        
        return self.create_user(school_id, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for CPSU health system
    Uses school_id instead of username for authentication
    """
    
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('staff', 'Clinic Staff'),
    ]
    
    DEPARTMENT_CHOICES = [
        ('College of Agriculture and Forestry', 'College of Agriculture and Forestry'),
        ('College of Teacher Education', 'College of Teacher Education'),
        ('College of Arts and Sciences', 'College of Arts and Sciences'),
        ('College of Hospitality Management', 'College of Hospitality Management'),
        ('College of Engineering', 'College of Engineering'),
        ('College of Computer Studies', 'College of Computer Studies'),
        ('College of Criminal Justice Education', 'College of Criminal Justice Education'),
    ]
    
    # Primary fields
    school_id = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
        help_text='School ID (immutable)'
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='student',
        help_text='User role (immutable)'
    )
    
    # Profile fields (editable for students)
    name = models.CharField(max_length=150, blank=True)
    department = models.CharField(
        max_length=100,
        choices=DEPARTMENT_CHOICES,
        blank=True
    )
    cpsu_address = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='CPSU Address'
    )
    
    # Django required fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    # Data consent
    data_consent_given = models.BooleanField(
        default=False,
        help_text='User consent for health data storage'
    )
    consent_date = models.DateTimeField(null=True, blank=True)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'school_id'
    REQUIRED_FIELDS = []  # Only school_id and password required
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['school_id']),
            models.Index(fields=['role']),
        ]
    
    def __str__(self):
        return f"{self.school_id} - {self.name} ({self.get_role_display()})"
    
    def save(self, *args, **kwargs):
        """Override save to set consent date"""
        if self.data_consent_given and not self.consent_date:
            self.consent_date = timezone.now()
        super().save(*args, **kwargs)


class SymptomRecord(models.Model):
    """
    Individual symptom report from a student
    Tracks duration, severity, and medication adherence
    """
    
    SEVERITY_CHOICES = [
        (1, 'Mild'),
        (2, 'Moderate'),
        (3, 'Severe'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='symptom_records',
        limit_choices_to={'role': 'student'}
    )
    
    # Symptom details
    symptoms = models.JSONField(
        help_text='List of symptom names (e.g., ["fever", "cough"])'
    )
    duration_days = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text='How many days symptoms have persisted'
    )
    severity = models.IntegerField(
        choices=SEVERITY_CHOICES,
        default=1
    )
    
    # ML prediction results
    predicted_disease = models.CharField(max_length=100, blank=True)
    confidence_score = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]
    )
    top_predictions = models.JSONField(
        null=True,
        blank=True,
        help_text='Top 3 predictions with confidence scores'
    )
    
    # Medication tracking
    on_medication = models.BooleanField(default=False)
    medication_adherence = models.BooleanField(
        null=True,
        blank=True,
        help_text='Is student following medication schedule?'
    )
    
    # Categorization (auto-tagged)
    is_communicable = models.BooleanField(default=False)
    is_acute = models.BooleanField(default=True)
    icd10_code = models.CharField(max_length=10, blank=True)
    
    # Hospital referral tracking
    requires_referral = models.BooleanField(default=False)
    referral_triggered = models.BooleanField(default=False)
    referral_date = models.DateTimeField(null=True, blank=True)

    # Staff override diagnosis
    staff_diagnosis = models.CharField(
        max_length=200,
        blank=True,
        default='',
        help_text='Final diagnosis set by clinic staff, overrides AI prediction'
    )
    final_diagnosis = models.CharField(
        max_length=200,
        blank=True,
        default='',
        help_text='Resolved final diagnosis (staff_diagnosis if set, otherwise predicted_disease)'
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'symptom_records'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['student', '-created_at']),
            models.Index(fields=['predicted_disease']),
            models.Index(fields=['requires_referral']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.student.school_id} - {self.predicted_disease or 'Pending'} ({self.created_at.date()})"
    
    def check_referral_criteria(self):
        """
        Check if student meets hospital referral criteria
        Trigger: 5+ symptom reports within 30 days
        """
        from datetime import timedelta
        
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_reports = SymptomRecord.objects.filter(
            student=self.student,
            created_at__gte=thirty_days_ago
        ).count()
        
        if recent_reports >= 5:
            self.requires_referral = True
            if not self.referral_triggered:
                self.referral_triggered = True
                self.referral_date = timezone.now()
        
        return self.requires_referral


class FollowUpManager(models.Manager):
    """Custom manager that auto-updates overdue follow-ups"""
    
    def get_queryset(self):
        return super().get_queryset()
    
    def update_overdue(self):
        """Update all overdue follow-ups in the database"""
        from datetime import date
        return self.get_queryset().filter(
            status='pending', 
            scheduled_date__lt=date.today()
        ).update(status='overdue')
    
    def pending_or_overdue(self):
        """Get all follow-ups that need attention (auto-updates overdue status first)"""
        self.update_overdue()  # Mark overdue items before querying
        return self.get_queryset().filter(status__in=['pending', 'overdue'])
    
    def needs_response(self, student):
        """Get follow-ups for a specific student that need response"""
        return self.pending_or_overdue().filter(student=student)


class FollowUp(models.Model):
    """
    Automated follow-up tracking for symptom reports
    Auto-scheduled after symptom submission to track recovery
    """
    
    STATUS_CHOICES = [
        ('pending', 'Pending Response'),
        ('completed', 'Completed'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]
    
    OUTCOME_CHOICES = [
        ('improved', 'Condition Improved'),
        ('same', 'No Change'),
        ('worse', 'Condition Worsened'),
        ('resolved', 'Fully Recovered'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    symptom_record = models.ForeignKey(
        'SymptomRecord',
        on_delete=models.CASCADE,
        related_name='follow_ups'
    )
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follow_ups',
        limit_choices_to={'role': 'student'}
    )
    
    # Scheduling
    scheduled_date = models.DateField(
        help_text='When follow-up is due (auto: 3 days after symptom report)'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    # Response data (filled by student)
    response_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When student responded to follow-up'
    )
    outcome = models.CharField(
        max_length=20,
        choices=OUTCOME_CHOICES,
        null=True,
        blank=True
    )
    notes = models.TextField(
        blank=True,
        help_text='Student notes on recovery progress'
    )
    still_experiencing_symptoms = models.BooleanField(
        null=True,
        blank=True,
        help_text='Are original symptoms still present?'
    )
    new_symptoms = models.JSONField(
        default=list,
        blank=True,
        help_text='Any new symptoms developed since last report'
    )
    
    # Staff review
    reviewed_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_followups',
        limit_choices_to={'role': 'staff'}
    )
    review_notes = models.TextField(
        blank=True,
        help_text='Staff review notes'
    )
    requires_appointment = models.BooleanField(
        default=False,
        help_text='Does student need clinic visit?'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Custom manager with auto-overdue check
    objects = FollowUpManager()
    
    class Meta:
        db_table = 'follow_ups'
        verbose_name = 'Follow-Up'
        verbose_name_plural = 'Follow-Ups'
        ordering = ['scheduled_date', '-created_at']
        indexes = [
            models.Index(fields=['student', 'status', 'scheduled_date']),
            models.Index(fields=['scheduled_date', 'status']),
            models.Index(fields=['symptom_record']),
        ]
    
    def __str__(self):
        return f"Follow-up: {self.student.name} - {self.scheduled_date} ({self.get_status_display()})"
    
    def check_overdue(self):
        """Check if follow-up is overdue and update status"""
        from datetime import date
        
        if self.status == 'pending' and self.scheduled_date < date.today():
            self.status = 'overdue'
            self.save()
        
        return self.status == 'overdue'
    
    @classmethod
    def create_from_symptom(cls, symptom_record, days_ahead=3):
        """
        Auto-create follow-up scheduled N days after symptom report
        Default: 3 days ahead
        """
        from datetime import timedelta, date
        
        scheduled_date = date.today() + timedelta(days=days_ahead)
        
        follow_up = cls.objects.create(
            symptom_record=symptom_record,
            student=symptom_record.student,
            scheduled_date=scheduled_date
        )
        
        return follow_up


class HealthInsight(models.Model):
    """
    AI-generated health insights from chat sessions
    Session-based, not persistent across chats
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='health_insights',
        limit_choices_to={'role': 'student'}
    )
    session_id = models.UUIDField(
        db_index=True,
        help_text='Chat session identifier'
    )
    
    # Insight content
    insight_text = models.TextField()
    references = models.JSONField(
        default=list,
        help_text='Medical references/sources for insight'
    )
    reliability_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text='Confidence in insight accuracy (0-1)'
    )
    
    # Metadata
    generated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'health_insights'
        ordering = ['-reliability_score', '-generated_at']
        indexes = [
            models.Index(fields=['student', 'session_id']),
            models.Index(fields=['session_id']),
        ]
    
    def __str__(self):
        return f"Insight for {self.student.school_id} (Score: {self.reliability_score:.2f})"


class ChatSession(models.Model):
    """
    Track AI chat sessions - metadata only, no conversation history
    Conversations are real-time and not persisted
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='chat_sessions',
        limit_choices_to={'role': 'student'}
    )
    
    # Session metadata
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.PositiveIntegerField(default=0)
    
    # Language used
    language = models.CharField(
        max_length=20,
        default='english',
        help_text='Chat language (English, Filipino, local dialect)'
    )
    
    # Session summary (not full transcript)
    topics_discussed = models.JSONField(
        default=list,
        help_text='Topics covered in session'
    )
    insights_generated_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        db_table = 'chat_sessions'
        ordering = ['-started_at']
        indexes = [
            models.Index(fields=['student', '-started_at']),
        ]
    
    def __str__(self):
        return f"Session {self.id} - {self.student.school_id} ({self.started_at.date()})"


class ConsentLog(models.Model):
    """
    Audit log for data consent changes
    Tracks when users grant/revoke consent
    """
    
    ACTION_CHOICES = [
        ('granted', 'Consent Granted'),
        ('revoked', 'Consent Revoked'),
        ('updated', 'Consent Updated'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='consent_logs'
    )
    
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'consent_logs'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.user.school_id} - {self.action} ({self.timestamp})"


class AuditLog(models.Model):
    """
    Security audit log for sensitive actions
    Tracks data access and modifications
    """
    
    ACTION_TYPES = [
        ('view', 'Viewed Record'),
        ('create', 'Created Record'),
        ('update', 'Updated Record'),
        ('delete', 'Deleted Record'),
        ('export', 'Exported Data'),
        ('login', 'User Login'),
        ('logout', 'User Logout'),
        ('failed_login', 'Failed Login Attempt'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Who
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='audit_logs'
    )
    
    # What
    action = models.CharField(max_length=20, choices=ACTION_TYPES)
    model_name = models.CharField(max_length=50, blank=True)
    object_id = models.CharField(max_length=50, blank=True)
    changes = models.JSONField(
        default=dict,
        help_text='What changed (before/after values)'
    )
    
    # When & Where
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    # Additional context
    success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)
    
    class Meta:
        db_table = 'audit_logs'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['action', '-timestamp']),
            models.Index(fields=['-timestamp']),
        ]
    
    def __str__(self):
        user_id = self.user.school_id if self.user else 'Anonymous'
        return f"{user_id} - {self.action} ({self.timestamp})"


class DepartmentStats(models.Model):
    """
    Cached department-level statistics for clinic dashboard
    Updated periodically to avoid heavy queries
    """
    
    department = models.CharField(max_length=100, unique=True, db_index=True)
    
    # Student counts
    total_students = models.PositiveIntegerField(default=0)
    students_with_symptoms = models.PositiveIntegerField(default=0)
    percentage_with_symptoms = models.FloatField(default=0.0)
    
    # Top diseases
    top_diseases = models.JSONField(
        default=list,
        help_text='[{"disease": "name", "count": N}, ...]'
    )
    
    # Symptom trends
    communicable_count = models.PositiveIntegerField(default=0)
    non_communicable_count = models.PositiveIntegerField(default=0)
    acute_count = models.PositiveIntegerField(default=0)
    chronic_count = models.PositiveIntegerField(default=0)
    
    # Referrals
    referral_pending_count = models.PositiveIntegerField(default=0)
    
    # Cache metadata
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'department_stats'
        verbose_name = 'Department Statistics'
        verbose_name_plural = 'Department Statistics'
    
    def __str__(self):
        return f"{self.department} Stats (Updated: {self.last_updated.date()})"


class EmergencyAlert(models.Model):
    """
    Emergency SOS alerts from students
    Critical for campus safety - immediate staff notification
    """
    
    STATUS_CHOICES = [
        ('active', 'Active - Needs Response'),
        ('responding', 'Staff Responding'),
        ('resolved', 'Resolved'),
        ('false_alarm', 'False Alarm'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='emergency_alerts',
        limit_choices_to={'role': 'student'}
    )
    
    # Emergency details
    location = models.CharField(
        max_length=255,
        help_text='Building/room where emergency occurred'
    )
    symptoms = models.JSONField(
        default=list,
        help_text='Emergency symptoms if any'
    )
    description = models.TextField(
        blank=True,
        help_text='Additional details from student'
    )
    
    # Status tracking
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )
    priority = models.IntegerField(
        default=100,
        help_text='Priority score (100 = critical)'
    )
    
    # Response tracking
    responded_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='emergency_responses',
        limit_choices_to={'role': 'staff'}
    )
    response_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When staff first responded'
    )
    resolved_at = models.DateTimeField(
        null=True,
        blank=True
    )
    resolution_notes = models.TextField(
        blank=True,
        help_text='Staff notes on resolution'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'emergency_alerts'
        verbose_name = 'Emergency Alert'
        verbose_name_plural = 'Emergency Alerts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['student', '-created_at']),
        ]
    
    def __str__(self):
        return f"Emergency: {self.student.name} at {self.location} ({self.get_status_display()})"
    
    def resolve(self, staff_user, notes=''):
        """Mark emergency as resolved"""
        self.status = 'resolved'
        self.resolved_at = timezone.now()
        self.responded_by = staff_user
        self.resolution_notes = notes
        self.save()
    
    @property
    def response_time_minutes(self):
        """Calculate response time in minutes"""
        if self.response_time:
            delta = self.response_time - self.created_at
            return int(delta.total_seconds() / 60)
        return None


class Medication(models.Model):
    """
    Medication prescribed by clinic staff to students
    Tracks medication details, dosage schedule, and duration
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='medications',
        limit_choices_to={'role': 'student'}
    )
    prescribed_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='prescribed_medications',
        limit_choices_to={'role': 'staff'}
    )
    
    # Medication details
    name = models.CharField(
        max_length=200,
        help_text='Medication name (e.g., Paracetamol, Amoxicillin)'
    )
    dosage = models.CharField(
        max_length=100,
        help_text='Dosage amount (e.g., 500mg, 2 tablets)'
    )
    frequency = models.CharField(
        max_length=50,
        help_text='How often (e.g., 3x daily, every 8 hours, as needed)'
    )
    schedule_times = models.JSONField(
        default=list,
        help_text='Specific times to take medication ["08:00", "14:00", "20:00"]'
    )
    
    # Duration
    start_date = models.DateField(
        help_text='When to start taking medication'
    )
    end_date = models.DateField(
        help_text='When to stop taking medication'
    )
    
    # Instructions
    instructions = models.TextField(
        blank=True,
        help_text='Special instructions (e.g., take with food, avoid alcohol)'
    )
    purpose = models.CharField(
        max_length=200,
        blank=True,
        help_text='What condition this treats'
    )
    
    # Status
    is_active = models.BooleanField(
        default=True,
        help_text='Whether medication is currently active'
    )
    
    # Linked to symptom record (optional)
    symptom_record = models.ForeignKey(
        SymptomRecord,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='prescribed_medications'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'medications'
        verbose_name = 'Medication'
        verbose_name_plural = 'Medications'
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['student', 'is_active']),
            models.Index(fields=['start_date', 'end_date']),
        ]
    
    def __str__(self):
        return f"{self.name} for {self.student.name} ({self.dosage}, {self.frequency})"
    
    @property
    def is_current(self):
        """Check if medication is currently active based on dates"""
        today = timezone.now().date()
        return self.is_active and self.start_date <= today <= self.end_date
    
    @property
    def days_remaining(self):
        """Calculate days remaining in medication course"""
        if not self.is_current:
            return 0
        delta = self.end_date - timezone.now().date()
        return max(0, delta.days)


class MedicationLog(models.Model):
    """
    Log of medication intake - tracks adherence
    Each scheduled dose creates a log entry
    """
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('taken', 'Taken'),
        ('missed', 'Missed'),
        ('skipped', 'Skipped'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    medication = models.ForeignKey(
        Medication,
        on_delete=models.CASCADE,
        related_name='logs'
    )
    
    # Schedule
    scheduled_date = models.DateField(
        help_text='Date medication should be taken'
    )
    scheduled_time = models.TimeField(
        help_text='Time medication should be taken'
    )
    
    # Actual intake
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    taken_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When medication was actually taken'
    )
    
    # Notes
    notes = models.TextField(
        blank=True,
        help_text='Student notes (e.g., felt nauseous, forgot)'
    )
    
    # Reminder sent
    reminder_sent = models.BooleanField(
        default=False,
        help_text='Whether reminder notification was sent'
    )
    reminder_sent_at = models.DateTimeField(
        null=True,
        blank=True
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'medication_logs'
        verbose_name = 'Medication Log'
        verbose_name_plural = 'Medication Logs'
        ordering = ['-scheduled_date', '-scheduled_time']
        unique_together = ['medication', 'scheduled_date', 'scheduled_time']
        indexes = [
            models.Index(fields=['medication', 'status']),
            models.Index(fields=['scheduled_date', 'scheduled_time']),
        ]
    
    def __str__(self):
        return f"{self.medication.name} - {self.scheduled_date} {self.scheduled_time} ({self.get_status_display()})"
    
    def mark_as_taken(self, notes=''):
        """Mark medication as taken"""
        self.status = 'taken'
        self.taken_at = timezone.now()
        self.notes = notes
        self.save()
    
    @property
    def is_overdue(self):
        """Check if dose is overdue"""
        if self.status != 'pending':
            return False
        now = timezone.now()
        scheduled_datetime = timezone.make_aware(
            timezone.datetime.combine(self.scheduled_date, self.scheduled_time)
        )
        return now > scheduled_datetime

class Message(models.Model):
    """
    Direct messaging between students and staff
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    recipient = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'messages'
        ordering = ['timestamp']
        indexes = [
            models.Index(fields=['sender', 'recipient', 'timestamp']),
            models.Index(fields=['recipient', 'is_read']),
        ]

    def __str__(self):
        return f"Message from {self.sender.school_id} to {self.recipient.school_id}"


class Appointment(models.Model):
    """
    Clinic appointments management
    """
    STATUS_CHOICES = [
        ('pending', 'Pending Confirmation'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='appointments',
        limit_choices_to={'role': 'student'}
    )
    staff = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='staff_appointments',
        limit_choices_to={'role': 'staff'}
    )

    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()

    purpose = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'appointments'
        ordering = ['scheduled_date', 'scheduled_time']
        indexes = [
            models.Index(fields=['student', 'status']),
            models.Index(fields=['scheduled_date', 'scheduled_time']),
        ]

    def __str__(self):
        return f"Appointment: {self.student.school_id} on {self.scheduled_date}"
