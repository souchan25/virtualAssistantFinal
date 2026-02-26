"""
Serializers for CPSU Health Assistant API
Handles data validation and transformation
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    SymptomRecord, HealthInsight, ChatSession, 
    ConsentLog, AuditLog, DepartmentStats, EmergencyAlert,
    Medication, MedicationLog, FollowUp
)

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['school_id', 'password', 'password_confirm', 'name', 'department', 'cpsu_address', 'email', 'role', 'data_consent_given']
        extra_kwargs = {
            'role': {'read_only': True},  # Role is set based on context, not user input
        }
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords must match"})
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile (read/update)"""
    
    class Meta:
        model = User
        fields = ['id', 'school_id', 'name', 'department', 'cpsu_address', 'role', 'data_consent_given', 'consent_date', 'date_joined', 'is_superuser']
        read_only_fields = ['id', 'school_id', 'role', 'consent_date', 'date_joined', 'is_superuser']


class SymptomRecordSerializer(serializers.ModelSerializer):
    """Serializer for symptom records"""
    student_school_id = serializers.CharField(source='student.school_id', read_only=True)
    student_name = serializers.CharField(source='student.name', read_only=True)
    
    class Meta:
        model = SymptomRecord
        fields = [
            'id', 'student', 'student_school_id', 'student_name',
            'symptoms', 'duration_days', 'severity',
            'predicted_disease', 'confidence_score', 'top_predictions',
            'on_medication', 'medication_adherence',
            'is_communicable', 'is_acute', 'icd10_code',
            'requires_referral', 'referral_triggered', 'referral_date',
            'staff_diagnosis', 'final_diagnosis',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'student', 'predicted_disease', 'confidence_score', 'top_predictions',
            'is_communicable', 'is_acute', 'icd10_code',
            'requires_referral', 'referral_triggered', 'referral_date',
            'created_at', 'updated_at'
        ]
    
    def to_representation(self, instance):
        """Ensure confidence is named correctly for frontend"""
        data = super().to_representation(instance)
        # Add confidence field for frontend compatibility
        data['confidence'] = data.get('confidence_score')
        return data


class SymptomSubmissionSerializer(serializers.Serializer):
    """Serializer for symptom submission endpoint"""
    symptoms = serializers.ListField(
        child=serializers.CharField(max_length=100),
        min_length=1,
        help_text='List of symptom names'
    )
    duration_days = serializers.IntegerField(min_value=1, default=1, required=False)
    severity = serializers.ChoiceField(
        choices=[(1, 'Mild'), (2, 'Moderate'), (3, 'Severe')],
        default=2,
        required=False
    )
    on_medication = serializers.BooleanField(default=False, required=False)
    medication_adherence = serializers.BooleanField(required=False, allow_null=True)
    patient_age = serializers.IntegerField(min_value=1, max_value=120, required=False, allow_null=True)
    patient_sex = serializers.ChoiceField(
        choices=[('male', 'Male'), ('female', 'Female')],
        required=False,
        allow_blank=True,
        default=''
    )


class DiseasePredictionSerializer(serializers.Serializer):
    """Serializer for disease prediction response"""
    predicted_disease = serializers.CharField()
    confidence_score = serializers.FloatField()
    top_predictions = serializers.ListField()
    description = serializers.CharField(allow_blank=True)
    precautions = serializers.ListField()
    is_communicable = serializers.BooleanField()
    is_acute = serializers.BooleanField()
    icd10_code = serializers.CharField(allow_blank=True)


class HealthInsightSerializer(serializers.ModelSerializer):
    """Serializer for AI health insights"""
    
    class Meta:
        model = HealthInsight
        fields = ['id', 'session_id', 'insight_text', 'references', 'reliability_score', 'generated_at']
        read_only_fields = ['id', 'generated_at']


class ChatSessionSerializer(serializers.ModelSerializer):
    """Serializer for chat sessions"""
    insights = HealthInsightSerializer(many=True, read_only=True, source='student.health_insights')
    
    class Meta:
        model = ChatSession
        fields = ['id', 'started_at', 'ended_at', 'duration_seconds', 'language', 'topics_discussed', 'insights_generated_count', 'insights']
        read_only_fields = ['id', 'started_at', 'insights_generated_count']


class ChatMessageSerializer(serializers.Serializer):
    """Serializer for real-time chat messages"""
    message = serializers.CharField(max_length=2000)
    language = serializers.ChoiceField(
        choices=['english', 'filipino', 'cebuano', 'tagalog'],
        default='english'
    )
    session_id = serializers.UUIDField(required=False)


class ConsentLogSerializer(serializers.ModelSerializer):
    """Serializer for consent logs"""
    
    class Meta:
        model = ConsentLog
        fields = ['id', 'action', 'ip_address', 'user_agent', 'timestamp']
        read_only_fields = ['id', 'timestamp']


class AuditLogSerializer(serializers.ModelSerializer):
    """Serializer for audit logs (staff only)"""
    user_school_id = serializers.CharField(source='user.school_id', read_only=True)
    
    class Meta:
        model = AuditLog
        fields = [
            'id', 'user', 'user_school_id', 'action', 'model_name', 'object_id',
            'changes', 'timestamp', 'ip_address', 'user_agent', 'success', 'error_message'
        ]
        read_only_fields = ['id', 'timestamp']


class DepartmentStatsSerializer(serializers.ModelSerializer):
    """Serializer for department statistics"""
    
    class Meta:
        model = DepartmentStats
        fields = [
            'department', 'total_students', 'students_with_symptoms', 'percentage_with_symptoms',
            'top_diseases', 'communicable_count', 'non_communicable_count',
            'acute_count', 'chronic_count', 'referral_pending_count', 'last_updated'
        ]
        read_only_fields = ['last_updated']


class DashboardStatsSerializer(serializers.Serializer):
    """Serializer for clinic dashboard overview"""
    total_students = serializers.IntegerField()
    students_with_symptoms_today = serializers.IntegerField()
    students_with_symptoms_7days = serializers.IntegerField()
    students_with_symptoms_30days = serializers.IntegerField()
    top_insight = serializers.CharField(allow_blank=True)
    department_breakdown = DepartmentStatsSerializer(many=True)
    recent_symptoms = SymptomRecordSerializer(many=True)
    pending_referrals = serializers.IntegerField()


class EmergencyAlertSerializer(serializers.ModelSerializer):
    """Serializer for emergency alerts"""
    student_school_id = serializers.CharField(source='student.school_id', read_only=True)
    student_name = serializers.CharField(source='student.name', read_only=True)
    student_department = serializers.CharField(source='student.department', read_only=True)
    responded_by_name = serializers.CharField(source='responded_by.name', read_only=True, allow_null=True)
    response_time_minutes = serializers.IntegerField(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = EmergencyAlert
        fields = [
            'id', 'student_school_id', 'student_name', 'student_department',
            'location', 'symptoms', 'description', 'status', 'status_display',
            'priority', 'responded_by_name', 'response_time', 'response_time_minutes',
            'resolved_at', 'resolution_notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'response_time_minutes']


class EmergencyTriggerSerializer(serializers.Serializer):
    """Serializer for triggering emergency alert"""
    location = serializers.CharField(max_length=255, required=True)
    symptoms = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=list
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        default=''
    )


class MedicationLogSerializer(serializers.ModelSerializer):
    """Serializer for medication logs (adherence tracking)"""
    medication_name = serializers.CharField(source='medication.name', read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = MedicationLog
        fields = [
            'id', 'medication', 'medication_name', 'scheduled_date', 
            'scheduled_time', 'status', 'status_display', 'taken_at', 
            'notes', 'reminder_sent', 'is_overdue', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'reminder_sent']


class MedicationSerializer(serializers.ModelSerializer):
    """Serializer for medications"""
    student_school_id = serializers.CharField(source='student.school_id', read_only=True)
    student_name = serializers.CharField(source='student.name', read_only=True)
    prescribed_by_name = serializers.CharField(source='prescribed_by.name', read_only=True, allow_null=True)
    is_current = serializers.BooleanField(read_only=True)
    days_remaining = serializers.IntegerField(read_only=True)
    
    # Include recent logs (optional)
    recent_logs = serializers.SerializerMethodField()
    adherence_rate = serializers.SerializerMethodField()
    
    class Meta:
        model = Medication
        fields = [
            'id', 'student', 'student_school_id', 'student_name',
            'prescribed_by', 'prescribed_by_name', 'name', 'dosage',
            'frequency', 'schedule_times', 'start_date', 'end_date',
            'instructions', 'purpose', 'is_active', 'is_current',
            'days_remaining', 'symptom_record', 'created_at', 'updated_at',
            'recent_logs', 'adherence_rate'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'prescribed_by']
    
    def get_recent_logs(self, obj):
        """Get last 7 logs"""
        logs = obj.logs.all()[:7]
        return MedicationLogSerializer(logs, many=True).data
    
    def get_adherence_rate(self, obj):
        """Calculate adherence percentage"""
        total_logs = obj.logs.exclude(status='pending').count()
        if total_logs == 0:
            return None
        taken_logs = obj.logs.filter(status='taken').count()
        return round((taken_logs / total_logs) * 100, 1)


class MedicationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating medications (staff only)"""
    
    class Meta:
        model = Medication
        fields = [
            'student', 'name', 'dosage', 'frequency', 'schedule_times',
            'start_date', 'end_date', 'instructions', 'purpose', 'symptom_record'
        ]
    
    def validate(self, data):
        """Validate dates"""
        if data['end_date'] < data['start_date']:
            raise serializers.ValidationError({
                'end_date': 'End date must be after start date'
            })
        return data


class FollowUpSerializer(serializers.ModelSerializer):
    """Serializer for follow-up records"""
    student_name = serializers.CharField(source='student.name', read_only=True)
    student_school_id = serializers.CharField(source='student.school_id', read_only=True)
    symptom_disease = serializers.CharField(source='symptom_record.predicted_disease', read_only=True)
    is_overdue = serializers.SerializerMethodField()
    days_until_due = serializers.SerializerMethodField()

    # Field aliases so the frontend field names match the model
    staff_notes = serializers.CharField(source='review_notes', read_only=True)
    student_response = serializers.CharField(source='notes', read_only=True)
    original_condition = serializers.CharField(source='symptom_record.predicted_disease', read_only=True)
    completed_at = serializers.DateTimeField(source='updated_at', read_only=True)
    reviewed_at = serializers.DateTimeField(source='updated_at', read_only=True)

    # Full symptom record details for the modal
    symptom_details = serializers.SerializerMethodField()

    class Meta:
        model = FollowUp
        fields = [
            'id', 'symptom_record', 'student', 'student_name', 'student_school_id',
            'symptom_disease', 'original_condition', 'scheduled_date', 'status',
            'response_date', 'outcome',
            'notes', 'student_response',
            'still_experiencing_symptoms', 'new_symptoms',
            'requires_appointment',
            'review_notes', 'staff_notes',
            'reviewed_at', 'completed_at',
            'is_overdue', 'days_until_due',
            'symptom_details',
            'created_at',
        ]
        read_only_fields = ['id', 'student', 'created_at']

    def get_is_overdue(self, obj):
        from datetime import date
        return obj.status == 'pending' and obj.scheduled_date < date.today()

    def get_days_until_due(self, obj):
        from datetime import date
        delta = obj.scheduled_date - date.today()
        return delta.days

    def get_symptom_details(self, obj):
        """Return full symptom record details for the review modal."""
        sr = obj.symptom_record
        if not sr:
            return None
        return {
            'id': str(sr.id),
            'symptoms': sr.symptoms or [],
            'duration_days': sr.duration_days,
            'severity': sr.severity,
            'predicted_disease': sr.predicted_disease,
            'confidence_score': sr.confidence_score,
            'top_predictions': sr.top_predictions or [],
            'is_communicable': sr.is_communicable,
            'is_acute': sr.is_acute,
            'icd10_code': sr.icd10_code,
            'requires_referral': sr.requires_referral,
            'staff_diagnosis': sr.staff_diagnosis,
            'final_diagnosis': sr.final_diagnosis,
            'on_medication': sr.on_medication,
            'created_at': sr.created_at.isoformat() if sr.created_at else None,
        }


class FollowUpResponseSerializer(serializers.Serializer):
    """Serializer for student follow-up responses"""
    outcome = serializers.ChoiceField(choices=FollowUp.OUTCOME_CHOICES)
    notes = serializers.CharField(required=False, allow_blank=True)
    still_experiencing_symptoms = serializers.BooleanField()
    new_symptoms = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=list
    )

from .models import Message, Appointment

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.name', read_only=True)
    recipient_name = serializers.CharField(source='recipient.name', read_only=True)
    sender_role = serializers.CharField(source='sender.role', read_only=True)
    recipient_role = serializers.CharField(source='recipient.role', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'sender_name', 'sender_role', 'recipient', 'recipient_name', 'recipient_role', 'content', 'is_read', 'timestamp']
        read_only_fields = ['id', 'sender', 'timestamp', 'is_read']

class AppointmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    student_school_id = serializers.CharField(source='student.school_id', read_only=True)
    staff_name = serializers.CharField(source='staff.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id', 'student', 'student_name', 'student_school_id',
            'staff', 'staff_name',
            'scheduled_date', 'scheduled_time',
            'purpose', 'notes', 'status', 'status_display',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
