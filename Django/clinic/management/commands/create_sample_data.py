"""
Management command to create sample test data
Usage: python manage.py create_sample_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from clinic.models import SymptomRecord, ChatSession, HealthInsight, DepartmentStats
import uuid

User = get_user_model()


class Command(BaseCommand):
    help = 'Create sample data for testing the application'
    
    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...\n')
        
        # Create sample students
        students = []
        departments = ['Computer Science', 'Engineering', 'Business', 'Nursing', 'Education']
        
        for i in range(5):
            student, created = User.objects.get_or_create(
                school_id=f'2024-{100+i:03d}',
                defaults={
                    'name': f'Student {i+1}',
                    'department': departments[i],
                    'cpsu_address': f'Dorm {(i % 3) + 1}',
                    'role': 'student',
                    'data_consent_given': True
                }
            )
            if created:
                student.set_password('student123')
                student.save()
                students.append(student)
                self.stdout.write(f'✓ Created student: {student.school_id}')
            else:
                students.append(student)
                self.stdout.write(f'  Student exists: {student.school_id}')
        
        # Create sample staff
        staff, created = User.objects.get_or_create(
            school_id='staff-001',
            defaults={
                'name': 'Clinic Staff',
                'department': 'Health Services',
                'role': 'staff',
                'is_staff': True
            }
        )
        if created:
            staff.set_password('staff123')
            staff.save()
            self.stdout.write('✓ Created staff user: staff-001')
        else:
            self.stdout.write('  Staff exists: staff-001')
        
        # Create sample symptom records
        sample_symptoms = [
            (['fever', 'cough', 'headache'], 'Common Cold', 0.85),
            (['high_fever', 'fatigue', 'body_ache'], 'Influenza', 0.92),
            (['stomach_pain', 'nausea', 'vomiting'], 'Gastroenteritis', 0.78),
            (['skin_rash', 'itching'], 'Allergy', 0.88),
            (['headache', 'dizziness'], 'Migraine', 0.81),
        ]
        
        for student, (symptoms, disease, confidence) in zip(students, sample_symptoms):
            record, created = SymptomRecord.objects.get_or_create(
                student=student,
                predicted_disease=disease,
                defaults={
                    'symptoms': symptoms,
                    'duration_days': 2,
                    'severity': 2,
                    'confidence_score': confidence,
                    'top_predictions': [
                        {'disease': disease, 'confidence': confidence},
                        {'disease': 'Other', 'confidence': 1 - confidence}
                    ],
                    'is_communicable': disease in ['Common Cold', 'Influenza'],
                    'is_acute': True
                }
            )
            if created:
                self.stdout.write(f'✓ Created symptom record for {student.school_id}: {disease}')
        
        # Create sample chat session
        for student in students[:2]:
            session, created = ChatSession.objects.get_or_create(
                student=student,
                defaults={
                    'language': 'english',
                    'duration_seconds': 300,
                    'topics_discussed': ['symptoms', 'treatment', 'precautions']
                }
            )
            
            if created:
                # Create sample insights for session
                insights_data = [
                    ('Monitor your symptoms closely and stay hydrated.', 0.92),
                    ('Get adequate rest for faster recovery.', 0.88),
                    ('Consult a doctor if symptoms worsen.', 0.95),
                ]
                
                for text, score in insights_data:
                    HealthInsight.objects.create(
                        student=student,
                        session_id=session.id,
                        insight_text=text,
                        reliability_score=score,
                        references=['WHO Guidelines', 'CDC Recommendations']
                    )
                
                self.stdout.write(f'✓ Created chat session with insights for {student.school_id}')
        
        # Create department stats
        for dept in departments:
            stats, created = DepartmentStats.objects.get_or_create(
                department=dept,
                defaults={
                    'total_students': 100,
                    'students_with_symptoms': 15,
                    'percentage_with_symptoms': 15.0,
                    'top_diseases': [
                        {'disease': 'Common Cold', 'count': 8},
                        {'disease': 'Flu', 'count': 5},
                        {'disease': 'Headache', 'count': 2}
                    ],
                    'communicable_count': 10,
                    'non_communicable_count': 5,
                    'acute_count': 12,
                    'chronic_count': 3,
                    'referral_pending_count': 0
                }
            )
            if created:
                self.stdout.write(f'✓ Created department stats for {dept}')
        
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('✅ Sample data created successfully!'))
        self.stdout.write('='*60)
        self.stdout.write('\nLogin credentials:')
        self.stdout.write('  Students: 2024-100 to 2024-104 / password: student123')
        self.stdout.write('  Staff: staff-001 / password: staff123\n')
