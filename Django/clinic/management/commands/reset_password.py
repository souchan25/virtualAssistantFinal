"""
Management command to reset user password
Usage: python manage.py reset_password <school_id>
"""

from django.core.management.base import BaseCommand
from clinic.models import CustomUser
from getpass import getpass


class Command(BaseCommand):
    help = 'Reset password for a user'

    def add_arguments(self, parser):
        parser.add_argument('school_id', type=str, help='User school ID')
        parser.add_argument('--password', type=str, help='New password (interactive if not provided)')

    def handle(self, *args, **options):
        school_id = options['school_id']
        password = options.get('password')
        
        try:
            user = CustomUser.objects.get(school_id=school_id)
        except CustomUser.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'❌ User with school_id "{school_id}" not found'))
            return
        
        # Interactive password input if not provided
        if not password:
            self.stdout.write(f'Resetting password for: {user.name} ({user.school_id})')
            password = getpass('New password: ')
            password2 = getpass('New password (again): ')
            
            if password != password2:
                self.stdout.write(self.style.ERROR('❌ Passwords do not match'))
                return
        
        # Set new password
        user.set_password(password)
        user.save()
        
        self.stdout.write(self.style.SUCCESS(f'✅ Password reset successfully for {user.school_id}'))
        self.stdout.write(f'   Name: {user.name}')
        self.stdout.write(f'   Role: {user.role}')
        self.stdout.write('')
        self.stdout.write('You can now login with:')
        self.stdout.write(f'   school_id: {school_id}')
        self.stdout.write(f'   password: (the one you just set)')
