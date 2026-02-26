from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from clinic.models import Message
from unittest.mock import patch
from django.db import IntegrityError

User = get_user_model()

class MessageTests(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(school_id='sender123', password='password123', role='student')
        self.recipient = User.objects.create_user(school_id='recipient456', password='password456', role='staff')
        self.client = APIClient()
        self.client.force_authenticate(user=self.sender)

    def test_send_message(self):
        url = '/api/messages/'
        data = {
            'recipient': self.recipient.id,
            'content': 'Hello from sender!'
        }
        response = self.client.post(url, data, format='json')
        # print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(Message.objects.get().content, 'Hello from sender!')

    def test_send_message_with_school_id(self):
        url = '/api/messages/'
        data = {
            'recipient': self.recipient.school_id,
            'content': 'Hello from sender!'
        }
        response = self.client.post(url, data, format='json')
        # print(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_message_error_handling(self):
        url = '/api/messages/'
        data = {
            'recipient': self.recipient.id,
            'content': 'Hello from sender!'
        }
        # Simulate a generic exception during save
        with patch('clinic.serializers.MessageSerializer.save', side_effect=Exception("Unknown error")):
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
            # Check safe error message
            self.assertIn(b'An internal error occurred', response.content)
            # Ensure details are not leaked
            self.assertNotIn(b'Unknown error', response.content)

    def test_create_message_integrity_error(self):
        url = '/api/messages/'
        data = {
            'recipient': self.recipient.id,
            'content': 'Hello from sender!'
        }
        # Simulate IntegrityError
        with patch('clinic.serializers.MessageSerializer.save', side_effect=IntegrityError("Constraint failed")):
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            # Check error message
            self.assertIn(b'Database integrity error', response.content)
