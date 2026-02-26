"""
Comprehensive tests for CPSU Health Assistant
Tests models, views, permissions, and ML integration
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import timedelta
import uuid

from .models import SymptomRecord, HealthInsight, ChatSession, ConsentLog, AuditLog
from .ml_service import get_ml_predictor

User = get_user_model()


# ============================================================================
# Model Tests
# ============================================================================

class CustomUserModelTests(TestCase):
    """Test custom user model"""
    
    def test_create_user(self):
        """Test creating a regular user"""
        user = User.objects.create_user(
            school_id='2024-001',
            password='testpass123',
            name='Test Student',
            department='College of Computer Studies'
        )
        
        self.assertEqual(user.school_id, '2024-001')
        self.assertEqual(user.name, 'Test Student')
        self.assertEqual(user.role, 'student')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.data_consent_given)
    
    def test_create_superuser(self):
        """Test creating a superuser"""
        admin = User.objects.create_superuser(
            school_id='admin001',
            password='admin123',
            name='Admin User',
            department='College of Computer Studies'
        )
        
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertEqual(admin.role, 'staff')
    
    def test_consent_date_auto_set(self):
        """Test that consent_date is set when consent is given"""
        user = User.objects.create_user(
            school_id='2024-002',
            password='pass123',
            name='Test User'
        )
        
        self.assertIsNone(user.consent_date)
        
        user.data_consent_given = True
        user.save()
        
        self.assertIsNotNone(user.consent_date)


class SymptomRecordTests(TestCase):
    """Test symptom record model"""
    
    def setUp(self):
        self.student = User.objects.create_user(
            school_id='2024-100',
            password='pass123',
            name='Test Student',
            department='Engineering',
            data_consent_given=True
        )
    
    def test_create_symptom_record(self):
        """Test creating a symptom record"""
        record = SymptomRecord.objects.create(
            student=self.student,
            symptoms=['fever', 'cough'],
            duration_days=3,
            severity=2,
            predicted_disease='Common Cold',
            confidence_score=0.85
        )
        
        self.assertEqual(record.student, self.student)
        self.assertEqual(record.duration_days, 3)
        self.assertEqual(record.severity, 2)
    
    def test_referral_criteria(self):
        """Test hospital referral logic (5+ reports in 30 days)"""
        # Create 4 records (should not trigger referral)
        for i in range(4):
            SymptomRecord.objects.create(
                student=self.student,
                symptoms=['headache'],
                duration_days=1,
                severity=1
            )
        
        record = SymptomRecord.objects.create(
            student=self.student,
            symptoms=['fever'],
            duration_days=2,
            severity=2
        )
        
        record.check_referral_criteria()
        self.assertFalse(record.requires_referral)
        
        # Create 5th record (should trigger referral)
        record_5th = SymptomRecord.objects.create(
            student=self.student,
            symptoms=['cough'],
            duration_days=1,
            severity=1
        )
        
        record_5th.check_referral_criteria()
        self.assertTrue(record_5th.requires_referral)


# ============================================================================
# API Tests
# ============================================================================

class AuthenticationAPITests(APITestCase):
    """Test authentication endpoints"""
    
    def test_user_registration(self):
        """Test user registration"""
        data = {
            'school_id': '2024-200',
            'password': 'securepass123',
            'password_confirm': 'securepass123',
            'name': 'New Student',
            'department': 'College of Hospitality Management',
            'cpsu_address': 'Dorm 1',
            'data_consent_given': True
        }
        
        response = self.client.post('/api/auth/register/', data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)
        
        # Verify user was created
        user = User.objects.get(school_id='2024-200')
        self.assertEqual(user.name, 'New Student')
        self.assertTrue(user.data_consent_given)
    
    def test_user_login(self):
        """Test user login"""
        # Create user
        user = User.objects.create_user(
            school_id='2024-201',
            password='testpass123',
            name='Login Test'
        )
        
        # Login
        data = {
            'school_id': '2024-201',
            'password': 'testpass123'
        }
        
        response = self.client.post('/api/auth/login/', data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
    
    def test_user_logout(self):
        """Test user logout"""
        user = User.objects.create_user(
            school_id='2024-202',
            password='pass123'
        )
        
        self.client.force_authenticate(user=user)
        response = self.client.post('/api/auth/logout/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProfileAPITests(APITestCase):
    """Test profile management endpoints"""
    
    def setUp(self):
        self.student = User.objects.create_user(
            school_id='2024-300',
            password='pass123',
            name='Profile Test',
            department='Engineering',
            cpsu_address='Dorm 2'
        )
        self.client.force_authenticate(user=self.student)
    
    def test_get_profile(self):
        """Test retrieving user profile"""
        response = self.client.get('/api/profile/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['school_id'], '2024-300')
        self.assertEqual(response.data['name'], 'Profile Test')
    
    def test_update_profile(self):
        """Test updating editable fields"""
        data = {
            'name': 'Updated Name',
            'department': 'College of Computer Studies',
            'cpsu_address': 'Dorm 3'
        }
        
        response = self.client.patch('/api/profile/', data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.student.refresh_from_db()
        self.assertEqual(self.student.name, 'Updated Name')
    
    def test_cannot_modify_immutable_fields(self):
        """Test that school_id and role cannot be modified"""
        data = {
            'school_id': '9999-999',  # Attempt to change
            'role': 'staff'  # Attempt to change
        }
        
        response = self.client.patch('/api/profile/', data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.student.refresh_from_db()
        self.assertEqual(self.student.school_id, '2024-300')  # Unchanged
    
    def test_update_consent(self):
        """Test updating data consent"""
        data = {'data_consent_given': True}
        
        response = self.client.post('/api/profile/consent/', data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.student.refresh_from_db()
        self.assertTrue(self.student.data_consent_given)
        self.assertIsNotNone(self.student.consent_date)


class SymptomSubmissionAPITests(APITestCase):
    """Test symptom submission and ML prediction"""
    
    def setUp(self):
        self.student = User.objects.create_user(
            school_id='2024-400',
            password='pass123',
            name='ML Test',
            data_consent_given=True
        )
        self.client.force_authenticate(user=self.student)
    
    def test_submit_symptoms_requires_consent(self):
        """Test that symptom submission requires data consent"""
        # Create user without consent
        no_consent_user = User.objects.create_user(
            school_id='2024-401',
            password='pass123',
            name='No Consent',
            data_consent_given=False
        )
        
        self.client.force_authenticate(user=no_consent_user)
        
        data = {
            'symptoms': ['fever', 'cough'],
            'duration_days': 2,
            'severity': 1
        }
        
        response = self.client.post('/api/symptoms/submit/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_submit_symptoms_success(self):
        """Test successful symptom submission"""
        data = {
            'symptoms': ['continuous_sneezing', 'shivering', 'chills'],
            'duration_days': 3,
            'severity': 2,
            'on_medication': False
        }
        
        response = self.client.post('/api/symptoms/submit/', data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('record_id', response.data)
        self.assertIn('prediction', response.data)
        
        # Verify record was created
        record = SymptomRecord.objects.get(id=response.data['record_id'])
        self.assertEqual(record.student, self.student)
        self.assertIsNotNone(record.predicted_disease)


class PermissionTests(APITestCase):
    """Test role-based access control"""
    
    def setUp(self):
        self.student = User.objects.create_user(
            school_id='2024-500',
            password='pass123',
            name='Student',
            role='student',
            data_consent_given=True
        )
        
        self.staff = User.objects.create_user(
            school_id='staff-001',
            password='pass123',
            name='Staff',
            role='staff'
        )
    
    def test_student_cannot_access_staff_endpoints(self):
        """Test students cannot access staff-only endpoints"""
        self.client.force_authenticate(user=self.student)
        
        response = self.client.get('/api/staff/dashboard/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_staff_can_access_staff_endpoints(self):
        """Test staff can access staff endpoints"""
        self.client.force_authenticate(user=self.staff)
        
        response = self.client.get('/api/staff/dashboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_student_can_only_see_own_records(self):
        """Test students can only view their own symptom records"""
        # Create records for student
        SymptomRecord.objects.create(
            student=self.student,
            symptoms=['fever'],
            duration_days=1,
            severity=1
        )
        
        # Create another student with records
        other_student = User.objects.create_user(
            school_id='2024-501',
            password='pass123',
            data_consent_given=True
        )
        SymptomRecord.objects.create(
            student=other_student,
            symptoms=['cough'],
            duration_days=1,
            severity=1
        )
        
        # Login as first student
        self.client.force_authenticate(user=self.student)
        
        response = self.client.get('/api/symptoms/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should only see own record
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['student'], self.student.id)


# ============================================================================
# ML Integration Tests
# ============================================================================

class MLPredictorTests(TestCase):
    """Test ML prediction service"""
    
    def test_predictor_loads_model(self):
        """Test that ML predictor loads successfully"""
        predictor = get_ml_predictor()
        
        self.assertIsNotNone(predictor.model)
        self.assertIsNotNone(predictor.feature_names)
    
    def test_prediction_with_symptoms(self):
        """Test disease prediction"""
        predictor = get_ml_predictor()
        
        symptoms = ['continuous_sneezing', 'shivering', 'chills']
        result = predictor.predict(symptoms)
        
        self.assertIn('predicted_disease', result)
        self.assertIn('confidence_score', result)
        self.assertIn('top_predictions', result)
        self.assertGreater(result['confidence_score'], 0.0)
    
    def test_get_available_symptoms(self):
        """Test retrieving available symptoms"""
        predictor = get_ml_predictor()
        
        symptoms = predictor.get_available_symptoms()
        
        self.assertIsInstance(symptoms, list)
        self.assertGreater(len(symptoms), 0)
