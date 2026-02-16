"""
URL Configuration for Clinic app
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, rasa_webhooks, admin_views

# Router for viewsets
router = DefaultRouter()
router.register(r'symptoms', views.SymptomRecordViewSet, basename='symptom')
router.register(r'audit', views.AuditLogViewSet, basename='audit')

app_name = 'clinic'

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', views.register_user, name='register'),
    path('auth/login/', views.login_user, name='login'),
    path('auth/logout/', views.logout_user, name='logout'),
    
    # User profile endpoints
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/consent/', views.update_consent, name='consent'),
    
    # Symptom & ML endpoints
    path('symptoms/submit/', views.submit_symptoms, name='submit-symptoms'),
    path('symptoms/available/', views.get_available_symptoms, name='available-symptoms'),
    
    # Rasa Webhook endpoints (for Rasa → Django ML integration)
    path('rasa/predict/', rasa_webhooks.rasa_webhook_predict, name='rasa-predict'),
    path('rasa/symptoms/', rasa_webhooks.rasa_webhook_symptoms, name='rasa-symptoms'),
    
    # AI Chat endpoints
    path('chat/start/', views.start_chat_session, name='start-chat'),
    path('chat/message/', views.send_chat_message, name='send-message'),
    path('chat/insights/', views.generate_insights, name='generate-insights'),
    path('chat/end/', views.end_chat_session, name='end-chat'),
    
    # Clinic staff endpoints
    path('staff/dashboard/', views.clinic_dashboard, name='dashboard'),
    path('staff/students/', views.student_directory, name='students'),
    path('staff/analytics/', views.staff_analytics, name='analytics'),
    path('staff/export/', views.export_report, name='export'),
    
    # Emergency SOS endpoints
    path('emergency/trigger/', views.trigger_emergency, name='emergency-trigger'),
    path('emergency/active/', views.emergency_active, name='emergency-active'),
    path('emergency/history/', views.emergency_history, name='emergency-history'),
    path('emergency/<uuid:emergency_id>/respond/', views.emergency_respond, name='emergency-respond'),
    path('emergency/<uuid:emergency_id>/resolve/', views.emergency_resolve, name='emergency-resolve'),
    
    # Medication Management endpoints
    path('medications/', views.medication_list, name='medication-list'),
    path('medications/create/', views.medication_create, name='medication-create'),
    path('medications/<uuid:medication_id>/', views.medication_detail, name='medication-detail'),
    path('medications/<uuid:medication_id>/update/', views.medication_update, name='medication-update'),
    path('medications/logs/today/', views.medication_logs_today, name='medication-logs-today'),
    path('medications/logs/<uuid:log_id>/taken/', views.medication_log_mark_taken, name='medication-log-taken'),
    path('medications/adherence/', views.medication_adherence, name='medication-adherence'),
    
    # Follow-Up endpoints
    path('followups/', views.followup_list, name='followup-list'),
    path('followups/pending/', views.followup_pending, name='followup-pending'),
    path('followups/<uuid:pk>/respond/', views.followup_respond, name='followup-respond'),
    path('followups/<uuid:pk>/review/', views.followup_review, name='followup-review'),
    path('followups/needs-review/', views.followup_needs_review, name='followup-needs-review'),
    
    # Admin custom views - Dashboard pages
    path('admin/monitoring/', admin_views.backend_monitoring_dashboard, name='admin-monitoring'),
    path('admin/users/', admin_views.admin_users_page, name='admin-users'),
    path('admin/health-records/', admin_views.admin_health_records_page, name='admin-health'),
    path('admin/api-analytics/', admin_views.admin_api_analytics_page, name='admin-analytics'),
    path('admin/settings/', admin_views.admin_settings_page, name='admin-settings'),
    
    # Router URLs (viewsets)
    path('', include(router.urls)),
]
