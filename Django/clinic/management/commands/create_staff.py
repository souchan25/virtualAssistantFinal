"""
Management command to create clinic staff users
Usage: python manage.py create_staff
"""

from django.core.management.base import BaseCommand
from clinic.models import CustomUser


class Command(BaseCommand):
    help = 'Create a clinic staff user (only school_id and password required)'

    def add_arguments(self, parser):
        parser.add_argument('--school_id', type=str, help='Staff school ID')
        parser.add_argument('--password', type=str, help='Staff password')
        parser.add_argument('--name', type=str, help='Staff name (optional)')
        parser.add_argument('--department', type=str, help='Department (optional)')

    def handle(self, *args, **options):
        school_id = options.get('school_id')
        password = options.get('password')
        name = options.get('name') or ''
        department = options.get('department') or ''

        # Interactive mode if arguments not provided
        if not school_id:
            school_id = input('School ID: ')
        if not password:
            from getpass import getpass
            password = getpass('Password: ')
            password2 = getpass('Password (again): ')
            if password != password2:
                self.stdout.write(self.style.ERROR('❌ Passwords do not match'))
                return

        # Check if user already exists
        if CustomUser.objects.filter(school_id=school_id).exists():
            self.stdout.write(self.style.ERROR(f'❌ User with school_id {school_id} already exists'))
            self.stdout.write(self.style.WARNING(f'   Use: python manage.py reset_password {school_id}'))
            return

        # Create staff user
        try:
            user = CustomUser.objects.create_user(
                school_id=school_id,
                password=password,
                name=name or f'Staff {school_id}',
                role='staff',
                department=department,
                is_staff=True,
                is_superuser=True,
                data_consent_given=True
            )
            
            self.stdout.write(self.style.SUCCESS(f'\n✅ Staff user created successfully!\n'))
            self.stdout.write(f'   School ID: {user.school_id}')
            self.stdout.write(f'   Name: {user.name}')
            self.stdout.write(f'   Role: {user.role}')
            if user.department:
                self.stdout.write(f'   Department: {user.department}')
            self.stdout.write('\n📝 Login credentials:')
            self.stdout.write(f'   school_id: {school_id}')
            self.stdout.write(f'   password: (hidden)\n')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error creating user: {str(e)}'))
