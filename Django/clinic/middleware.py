"""
Custom middleware for audit logging and security
"""

from django.utils.deprecation import MiddlewareMixin
from .models import AuditLog


def get_client_ip(request):
    """Extract client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class AuditMiddleware(MiddlewareMixin):
    """
    Middleware to log sensitive actions for security auditing
    Logs: logins, data exports, record access, modifications
    """
    
    AUDITABLE_PATHS = [
        '/api/auth/login',
        '/api/auth/logout',
        '/api/symptoms/',
        '/api/students/',
        '/api/export/',
    ]
    
    def process_request(self, request):
        """Store request metadata for later audit logging"""
        request.audit_data = {
            'ip_address': get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', '')[:255],
        }
        return None
    
    def process_response(self, request, response):
        """Log auditable actions after response is generated"""
        # Skip audit logging for non-auditable paths
        path = request.path
        should_audit = any(path.startswith(auditable) for auditable in self.AUDITABLE_PATHS)
        
        if not should_audit:
            return response
        
        # Skip if no user (anonymous access)
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            # Log failed login attempts
            if 'login' in path and response.status_code == 401:
                AuditLog.objects.create(
                    user=None,
                    action='failed_login',
                    ip_address=request.audit_data['ip_address'],
                    user_agent=request.audit_data['user_agent'],
                    success=False,
                    error_message='Invalid credentials'
                )
            return response
        
        # Determine action type
        action = self._get_action_type(request.method, path, response.status_code)
        
        if action:
            try:
                AuditLog.objects.create(
                    user=request.user,
                    action=action,
                    model_name=self._extract_model_name(path),
                    ip_address=request.audit_data['ip_address'],
                    user_agent=request.audit_data['user_agent'],
                    success=200 <= response.status_code < 300
                )
            except Exception as e:
                # Don't let audit logging break the application
                print(f"Audit log error: {e}")
        
        return response
    
    def _get_action_type(self, method, path, status_code):
        """Map HTTP method and path to audit action type"""
        if 'login' in path:
            if status_code == 200:
                return 'login'
            else:
                return 'failed_login'
        elif 'logout' in path:
            return 'logout'
        elif 'export' in path:
            return 'export'
        elif method == 'GET':
            return 'view'
        elif method == 'POST':
            return 'create'
        elif method in ['PUT', 'PATCH']:
            return 'update'
        elif method == 'DELETE':
            return 'delete'
        return None
    
    def _extract_model_name(self, path):
        """Extract model name from API path"""
        parts = path.strip('/').split('/')
        if len(parts) >= 2:
            return parts[1]  # e.g., '/api/symptoms/' -> 'symptoms'
        return ''
