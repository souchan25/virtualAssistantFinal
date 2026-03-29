"""
pytest configuration for Django tests
"""
import os
import django
from django.conf import settings

# Configure Django settings before any tests run
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_assistant.settings')

def pytest_configure():
    """Configure Django for pytest"""
    if not settings.configured:
        settings.configure(
            DEBUG=True,
            SECRET_KEY='test-secret-key-for-pytest',
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                }
            },
            INSTALLED_APPS=[
                'django.contrib.admin',
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'django.contrib.messages',
                'django.contrib.staticfiles',
                'rest_framework',
                'rest_framework.authtoken',
                'corsheaders',
                'clinic.apps.ClinicConfig',
            ],
            MIDDLEWARE=[
                'django.middleware.security.SecurityMiddleware',
                'django.contrib.sessions.middleware.SessionMiddleware',
                'corsheaders.middleware.CorsMiddleware',
                'django.middleware.common.CommonMiddleware',
                'django.middleware.csrf.CsrfViewMiddleware',
                'django.contrib.auth.middleware.AuthenticationMiddleware',
                'django.contrib.messages.middleware.MessageMiddleware',
                'django.middleware.clickjacking.XFrameOptionsMiddleware',
            ],
            ROOT_URLCONF='health_assistant.urls',
            REST_FRAMEWORK={
                'DEFAULT_AUTHENTICATION_CLASSES': [
                    'rest_framework.authentication.TokenAuthentication',
                ],
                'DEFAULT_THROTTLE_CLASSES': [
                    'rest_framework.throttling.AnonRateThrottle',
                    'rest_framework.throttling.UserRateThrottle',
                    'rest_framework.throttling.ScopedRateThrottle',
                ],
                'DEFAULT_THROTTLE_RATES': {
                    'anon': '100/day',
                    'user': '1000/day',
                    'auth': '10/min',
                },
            },
            USE_TZ=True,
        )
        django.setup()
