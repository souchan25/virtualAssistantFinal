"""
Django Admin configuration for Clinic app
Configured with Jazzmin for modern UI
Developer/Admin use only - For backend monitoring and staff account management

SECURITY NOTE:
All medical data (medications, alerts, follow-ups, symptoms, etc.) is HIDDEN from admin panel.
Only CustomUser model is exposed for:
- Creating clinic staff accounts
- Managing user permissions
- Monitoring backend flow and API usage (via logs)
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import CustomUser, AuditLog


# ========================================
# CUSTOM USER ADMIN (For Staff Accounts)
# ========================================
@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """
    Admin interface for managing user accounts
    Primary use: Creating clinic staff accounts
    """
    
    list_display = [
        'school_id', 'name', 'role', 'department', 
        'data_consent_status', 'account_status', 'date_joined'
    ]
    list_filter = ['role', 'data_consent_given', 'is_active', 'is_staff', 'department', 'date_joined']
    search_fields = ['school_id', 'name', 'department']
    ordering = ['-date_joined']
    list_per_page = 50
    
    # Custom colored status badges
    @admin.display(description='Consent Status', ordering='data_consent_given')
    def data_consent_status(self, obj):
        if obj.data_consent_given:
            return format_html(
                '<span style="color: white; background-color: #28a745; padding: 3px 10px; border-radius: 3px;">✓ Granted</span>'
            )
        return format_html(
            '<span style="color: white; background-color: #ffc107; padding: 3px 10px; border-radius: 3px;">⚠ Pending</span>'
        )
    
    @admin.display(description='Account Status', ordering='is_active')
    def account_status(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="color: white; background-color: #28a745; padding: 3px 10px; border-radius: 3px;">● Active</span>'
            )
        return format_html(
            '<span style="color: white; background-color: #dc3545; padding: 3px 10px; border-radius: 3px;">● Inactive</span>'
        )
    
    fieldsets = (
        ('🔐 Login Credentials', {
            'fields': ('school_id', 'password'),
            'description': 'School ID is used as username for login'
        }),
        ('👤 Personal Information', {
            'fields': ('name', 'department', 'cpsu_address')
        }),
        ('🛡️ Role & Permissions', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser'),
            'description': 'Set role to "clinic_staff" for clinic personnel'
        }),
        ('📋 Advanced Permissions (Optional)', {
            'classes': ('collapse',),
            'fields': ('groups', 'user_permissions'),
        }),
        ('✅ Data Consent', {
            'fields': ('data_consent_given', 'consent_date'),
            'description': 'Required for students to use health features'
        }),
        ('📅 Important Dates', {
            'classes': ('collapse',),
            'fields': ('last_login', 'date_joined')
        }),
    )
    
    add_fieldsets = (
        ('Create New User Account', {
            'classes': ('wide',),
            'fields': (
                'school_id', 'name', 'department', 'cpsu_address',
                'role', 'password1', 'password2', 'is_active', 'is_staff'
            ),
            'description': mark_safe(
                '<div style="background-color: #e3f2fd; padding: 15px; border-left: 4px solid #2196f3; margin-bottom: 20px;">'
                '<strong>Quick Guide:</strong><br>'
                '• <strong>School ID:</strong> Unique identifier (e.g., 2024-0001)<br>'
                '• <strong>Role:</strong> Choose "clinic_staff" for staff members<br>'
                '• <strong>Is Staff:</strong> Check this for admin panel access<br>'
                '</div>'
            )
        }),
    )
    
    readonly_fields = ['last_login', 'date_joined', 'consent_date']
    
    # Actions
    actions = ['activate_users', 'deactivate_users', 'grant_staff_access']
    
    @admin.action(description='✓ Activate selected users')
    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} user(s) activated successfully.')
    
    @admin.action(description='✗ Deactivate selected users')
    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} user(s) deactivated.')
    
    @admin.action(description='👔 Grant staff access')
    def grant_staff_access(self, request, queryset):
        updated = queryset.update(is_staff=True, role='clinic_staff')
        self.message_user(request, f'{updated} user(s) granted staff access.')


# ========================================
# AUDIT LOG ADMIN (Backend Monitoring)
# ========================================
@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """
    Backend monitoring and audit trail
    View API usage, errors, and system activity
    """
    
    list_display = [
        'timestamp', 'user_link', 'action_badge', 'model_name', 
        'success_badge', 'ip_address', 'error_preview'
    ]
    list_filter = [
        'action', 'success', 'timestamp', 'model_name'
    ]
    search_fields = [
        'user__school_id', 'user__name', 'model_name', 
        'ip_address', 'error_message'
    ]
    readonly_fields = [
        'id', 'user', 'action', 'model_name', 'object_id', 
        'changes', 'timestamp', 'ip_address', 'user_agent', 
        'success', 'error_message'
    ]
    date_hierarchy = 'timestamp'
    list_per_page = 100
    
    # Don't allow adding/editing audit logs
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        # Allow deleting old logs (cleanup)
        return request.user.is_superuser
    
    @admin.display(description='User', ordering='user__school_id')
    def user_link(self, obj):
        if obj.user:
            return format_html(
                '<span style="font-family: monospace;">{}</span>',
                obj.user.school_id
            )
        return format_html(
            '<span style="color: #6c757d; font-style: italic;">Anonymous</span>'
        )
    
    @admin.display(description='Action', ordering='action')
    def action_badge(self, obj):
        colors = {
            'view': '#17a2b8',      # Info
            'create': '#28a745',     # Success
            'update': '#ffc107',     # Warning
            'delete': '#dc3545',     # Danger
            'export': '#fd7e14',     # Orange
            'login': '#007bff',      # Primary
            'logout': '#6c757d',     # Secondary
            'failed_login': '#721c24' # Dark red
        }
        color = colors.get(obj.action, '#6c757d')
        label = obj.get_action_display()
        
        return format_html(
            '<span style="color: white; background-color: {}; padding: 3px 8px; '
            'border-radius: 3px; font-size: 11px; font-weight: bold;">{}</span>',
            color, label
        )
    
    @admin.display(description='Status', ordering='success')
    def success_badge(self, obj):
        if obj.success:
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">✓ Success</span>'
            )
        return format_html(
            '<span style="color: #dc3545; font-weight: bold;">✗ Failed</span>'
        )
    
    @admin.display(description='Error')
    def error_preview(self, obj):
        if obj.error_message:
            preview = obj.error_message[:80] + '...' if len(obj.error_message) > 80 else obj.error_message
            return format_html(
                '<span style="color: #dc3545; font-family: monospace; font-size: 11px;">{}</span>',
                preview
            )
        return '-'
    
    fieldsets = (
        ('📊 Audit Information', {
            'fields': ('id', 'timestamp', 'success')
        }),
        ('👤 User Details', {
            'fields': ('user', 'ip_address', 'user_agent')
        }),
        ('🎯 Action Details', {
            'fields': ('action', 'model_name', 'object_id', 'changes')
        }),
        ('❌ Error Information', {
            'fields': ('error_message',),
            'classes': ('collapse',)
        }),
    )
    
    # Custom admin actions
    actions = ['delete_old_logs']
    
    @admin.action(description='🗑️ Delete logs older than 90 days')
    def delete_old_logs(self, request, queryset):
        cutoff_date = timezone.now() - timedelta(days=90)
        deleted_count = AuditLog.objects.filter(timestamp__lt=cutoff_date).delete()[0]
        self.message_user(
            request, 
            f'Deleted {deleted_count} audit log(s) older than 90 days.'
        )


# ========================================
# ADMIN SITE CUSTOMIZATION
# ========================================
admin.site.site_header = "CPSU Health Assistant - Developer Admin"
admin.site.site_title = "CPSU Health Dev Admin"
admin.site.index_title = "Backend Monitoring & Staff Account Management"

# ========================================
# SECURITY & PRIVACY NOTES
# ========================================
# The following models are INTENTIONALLY NOT registered in admin (sensitive medical data):
# - Medication (prescription data)
# - MedicationLog (medication adherence records)
# - FollowUp (patient follow-up appointments)
# - EmergencyAlert (emergency medical alerts)
# - SymptomRecord (patient diagnosis data)
# - HealthInsight (AI-generated medical insights)
# - ChatSession (patient-AI chat conversations)
# - ConsentLog (privacy consent tracking)
# - AuditLog (system audit trails - use Django's logging for backend monitoring)
# - DepartmentStats (statistical aggregations)
#
# DEVELOPER RESPONSIBILITIES:
# 1. Create clinic staff accounts (role='clinic_staff', is_staff=True)
# 2. Monitor backend flow via Django logging and server logs
# 3. Monitor LLM API usage via provider dashboards (Gemini, OpenRouter, Cohere)
# 4. Manage user permissions and account status
#
# Medical data access is ONLY available to clinic staff through the Vue.js frontend.
# These can only be accessed via API or database directly.
