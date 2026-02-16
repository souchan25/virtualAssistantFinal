"""
Custom admin views for backend monitoring and dashboard
Provides dashboard with metrics, LLM usage, system health, and management pages
"""

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Count, Q
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from clinic.models import AuditLog, CustomUser, SymptomRecord, ChatSession
import os


@staff_member_required
def backend_monitoring_dashboard(request):
    """
    Custom dashboard showing:
    - Backend metrics (API latency, errors)
    - LLM API usage stats
    - System health indicators
    """
    
    # Time ranges
    now = timezone.now()
    last_24h = now - timedelta(hours=24)
    last_7d = now - timedelta(days=7)
    last_30d = now - timedelta(days=30)
    
    # User stats
    total_users = CustomUser.objects.count()
    active_users_24h = AuditLog.objects.filter(
        timestamp__gte=last_24h,
        action='login'
    ).values('user').distinct().count()
    
    staff_count = CustomUser.objects.filter(role='clinic_staff').count()
    student_count = CustomUser.objects.filter(role='student').count()
    
    # API Activity (Last 24 hours)
    api_logs_24h = AuditLog.objects.filter(timestamp__gte=last_24h)
    
    total_requests_24h = api_logs_24h.count()
    failed_requests_24h = api_logs_24h.filter(success=False).count()
    success_rate_24h = (
        ((total_requests_24h - failed_requests_24h) / total_requests_24h * 100)
        if total_requests_24h > 0 else 100
    )
    
    # Recent errors (Last 7 days)
    recent_errors = AuditLog.objects.filter(
        success=False,
        timestamp__gte=last_7d
    ).order_by('-timestamp')[:10]
    
    # Action breakdown (Last 24h)
    action_stats = api_logs_24h.values('action').annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    # Failed login attempts (security monitoring)
    failed_logins_24h = AuditLog.objects.filter(
        action='failed_login',
        timestamp__gte=last_24h
    ).count()
    
    # LLM API Configuration Status
    llm_providers = {
        'Gemini': {
            'configured': bool(os.getenv('GEMINI_API_KEY')),
            'tier': 'Free (1,500 req/day)',
            'dashboard': 'https://aistudio.google.com/apikey'
        },
        'OpenRouter (Qwen)': {
            'configured': bool(os.getenv('OPENROUTER_API_KEY')),
            'tier': 'Free (Limited)',
            'dashboard': 'https://openrouter.ai/activity'
        },
        'Groq (Grok 2)': {
            'configured': bool(os.getenv('GROQ_API_KEY')),
            'tier': 'Free (30 req/min)',
            'dashboard': 'https://console.groq.com/'
        },
        'Cohere': {
            'configured': bool(os.getenv('COHERE_API_KEY')),
            'tier': 'Free (100 req/min)',
            'dashboard': 'https://dashboard.cohere.com/'
        }
    }
    
    # System Health Indicators
    health_checks = {
        'Database': {
            'status': 'healthy',
            'details': f'{total_users} total users'
        },
        'ML Model': {
            'status': 'healthy' if settings.ML_MODEL_PATH.exists() else 'warning',
            'details': 'Loaded' if settings.ML_MODEL_PATH.exists() else 'Not found'
        },
        'LLM Providers': {
            'status': 'healthy' if any(p['configured'] for p in llm_providers.values()) else 'warning',
            'details': f"{sum(1 for p in llm_providers.values() if p['configured'])}/4 configured"
        }
    }
    
    context = {
        # User stats
        'total_users': total_users,
        'active_users_24h': active_users_24h,
        'staff_count': staff_count,
        'student_count': student_count,
        
        # API stats
        'total_requests_24h': total_requests_24h,
        'failed_requests_24h': failed_requests_24h,
        'success_rate_24h': round(success_rate_24h, 1),
        'failed_logins_24h': failed_logins_24h,
        
        # Recent data
        'recent_errors': recent_errors,
        'action_stats': action_stats,
        
        # LLM & Health
        'llm_providers': llm_providers,
        'health_checks': health_checks,
        
        # Meta
        'last_updated': now,
    }
    
    return render(request, 'admin/backend_monitoring.html', context)


@staff_member_required
def admin_users_page(request):
    """
    User management and directory page
    Shows student and staff accounts with activity
    """
    now = timezone.now()
    last_30d = now - timedelta(days=30)
    
    # User statistics
    total_users = CustomUser.objects.count()
    students = CustomUser.objects.filter(role='student')
    staff = CustomUser.objects.filter(role='clinic_staff')
    
    # Recent users
    recent_users = CustomUser.objects.all().order_by('-date_joined')[:20]
    
    # Active users in last 30 days
    active_user_ids = AuditLog.objects.filter(
        timestamp__gte=last_30d
    ).values_list('user_id', flat=True).distinct()
    
    # User activity summary
    user_activity = AuditLog.objects.filter(
        timestamp__gte=last_30d
    ).values('user').annotate(
        activity_count=Count('id')
    ).order_by('-activity_count')[:10]
    
    # Role distribution
    role_stats = CustomUser.objects.values('role').annotate(
        count=Count('id')
    )
    
    context = {
        'total_users': total_users,
        'student_count': students.count(),
        'staff_count': staff.count(),
        'recent_users': recent_users,
        'active_users_count': len(active_user_ids),
        'user_activity': user_activity,
        'role_stats': role_stats,
        'last_updated': now,
    }
    
    return render(request, 'admin/users.html', context)


@staff_member_required
def admin_health_records_page(request):
    """
    Health records and symptom data page
    Shows symptom submissions, predictions, and trends
    """
    now = timezone.now()
    last_7d = now - timedelta(days=7)
    last_30d = now - timedelta(days=30)
    
    # Symptom statistics
    total_records = SymptomRecord.objects.count()
    records_7d = SymptomRecord.objects.filter(created_at__gte=last_7d).count()
    records_30d = SymptomRecord.objects.filter(created_at__gte=last_30d).count()
    
    # Top predicted diseases (Last 30 days)
    top_diseases = SymptomRecord.objects.filter(
        created_at__gte=last_30d
    ).values('predicted_disease').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    # Prediction accuracy stats
    high_confidence = SymptomRecord.objects.filter(
        confidence__gte=0.8,
        created_at__gte=last_30d
    ).count()
    
    medium_confidence = SymptomRecord.objects.filter(
        confidence__lt=0.8,
        confidence__gte=0.6,
        created_at__gte=last_30d
    ).count()
    
    low_confidence = SymptomRecord.objects.filter(
        confidence__lt=0.6,
        created_at__gte=last_30d
    ).count()
    
    # Recent symptom records
    recent_records = SymptomRecord.objects.all().order_by('-created_at')[:15]
    
    context = {
        'total_records': total_records,
        'records_7d': records_7d,
        'records_30d': records_30d,
        'top_diseases': top_diseases,
        'high_confidence': high_confidence,
        'medium_confidence': medium_confidence,
        'low_confidence': low_confidence,
        'recent_records': recent_records,
        'last_updated': now,
    }
    
    return render(request, 'admin/health_records.html', context)


@staff_member_required
def admin_api_analytics_page(request):
    """
    API analytics and performance page
    Shows request metrics, endpoint usage, and error rates
    """
    now = timezone.now()
    last_7d = now - timedelta(days=7)
    last_30d = now - timedelta(days=30)
    
    # API metrics by time period
    metrics_7d = {
        'total_requests': AuditLog.objects.filter(timestamp__gte=last_7d).count(),
        'successful': AuditLog.objects.filter(timestamp__gte=last_7d, success=True).count(),
        'failed': AuditLog.objects.filter(timestamp__gte=last_7d, success=False).count(),
    }
    
    metrics_30d = {
        'total_requests': AuditLog.objects.filter(timestamp__gte=last_30d).count(),
        'successful': AuditLog.objects.filter(timestamp__gte=last_30d, success=True).count(),
        'failed': AuditLog.objects.filter(timestamp__gte=last_30d, success=False).count(),
    }
    
    # Calculate success rates
    if metrics_7d['total_requests'] > 0:
        metrics_7d['success_rate'] = round((metrics_7d['successful'] / metrics_7d['total_requests']) * 100, 1)
    else:
        metrics_7d['success_rate'] = 100
        
    if metrics_30d['total_requests'] > 0:
        metrics_30d['success_rate'] = round((metrics_30d['successful'] / metrics_30d['total_requests']) * 100, 1)
    else:
        metrics_30d['success_rate'] = 100
    
    # Top endpoints
    top_endpoints = AuditLog.objects.filter(
        timestamp__gte=last_30d
    ).values('action').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    # Error breakdown
    error_breakdown = AuditLog.objects.filter(
        success=False,
        timestamp__gte=last_30d
    ).values('error_message').annotate(
        count=Count('id')
    ).order_by('-count')[:8]
    
    # Recent errors
    recent_errors = AuditLog.objects.filter(
        success=False,
        timestamp__gte=last_7d
    ).order_by('-timestamp')[:10]
    
    context = {
        'metrics_7d': metrics_7d,
        'metrics_30d': metrics_30d,
        'top_endpoints': top_endpoints,
        'error_breakdown': error_breakdown,
        'recent_errors': recent_errors,
        'last_updated': now,
    }
    
    return render(request, 'admin/api_analytics.html', context)


@staff_member_required
def admin_settings_page(request):
    """
    Admin settings and configuration page
    Shows system configuration and LLM provider status
    """
    now = timezone.now()
    
    # LLM API Configuration Status
    llm_providers = {
        'Gemini': {
            'configured': bool(os.getenv('GEMINI_API_KEY')),
            'tier': 'Free (1,500 req/day)',
            'dashboard': 'https://aistudio.google.com/apikey',
            'icon': '🔵'
        },
        'OpenRouter (Qwen)': {
            'configured': bool(os.getenv('OPENROUTER_API_KEY')),
            'tier': 'Free (Limited)',
            'dashboard': 'https://openrouter.ai/activity',
            'icon': '🟢'
        },
        'Groq (Grok 2)': {
            'configured': bool(os.getenv('GROQ_API_KEY')),
            'tier': 'Free (30 req/min)',
            'dashboard': 'https://console.groq.com/',
            'icon': '⚫'
        },
        'Cohere': {
            'configured': bool(os.getenv('COHERE_API_KEY')),
            'tier': 'Free (100 req/min)',
            'dashboard': 'https://dashboard.cohere.com/',
            'icon': '🟡'
        }
    }
    
    # System information
    ml_model_exists = settings.ML_MODEL_PATH.exists()
    configured_providers = sum(1 for p in llm_providers.values() if p['configured'])
    
    # Database stats
    user_count = CustomUser.objects.count()
    symptom_count = SymptomRecord.objects.count()
    chat_count = ChatSession.objects.count()
    
    context = {
        'llm_providers': llm_providers,
        'ml_model_exists': ml_model_exists,
        'configured_providers': configured_providers,
        'total_providers': len(llm_providers),
        'user_count': user_count,
        'symptom_count': symptom_count,
        'chat_count': chat_count,
        'debug_mode': settings.DEBUG,
        'last_updated': now,
    }
    
    return render(request, 'admin/settings.html', context)
