"""
Management command to list and verify users
Usage: python manage.py check_users
"""

from django.core.management.base import BaseCommand
from clinic.models import CustomUser


class Command(BaseCommand):
    help = 'List all users and their details for debugging'

    def add_arguments(self, parser):
        parser.add_argument('--school_id', type=str, help='Filter by specific school_id')
        parser.add_argument('--role', type=str, choices=['student', 'staff'], help='Filter by role')

    def handle(self, *args, **options):
        queryset = CustomUser.objects.all()
        
        school_id = options.get('school_id')
        role = options.get('role')
        
        if school_id:
            queryset = queryset.filter(school_id=school_id)
        if role:
            queryset = queryset.filter(role=role)
        
        if not queryset.exists():
            self.stdout.write(self.style.WARNING('No users found'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'\n📋 Found {queryset.count()} user(s):\n'))
        
        for user in queryset:
            self.stdout.write('-' * 60)
            self.stdout.write(f'School ID:     {user.school_id}')
            self.stdout.write(f'Name:          {user.name or "(not set)"}')
            self.stdout.write(f'Role:          {user.role}')
            self.stdout.write(f'Department:    {user.department or "(not set)"}')
            self.stdout.write(f'Is Active:     {user.is_active}')
            self.stdout.write(f'Is Staff:      {user.is_staff}')
            self.stdout.write(f'Is Superuser:  {user.is_superuser}')
            self.stdout.write(f'Consent Given: {user.data_consent_given}')
            self.stdout.write(f'Has Password:  {user.has_usable_password()}')
            self.stdout.write(f'Date Joined:   {user.date_joined}')
            
        self.stdout.write('-' * 60)
        self.stdout.write('')
