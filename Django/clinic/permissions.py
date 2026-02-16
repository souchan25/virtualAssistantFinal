"""
Custom permissions for role-based access control
"""

from rest_framework import permissions


class IsStudent(permissions.BasePermission):
    """Allow access only to users with 'student' role"""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'student'


class IsClinicStaff(permissions.BasePermission):
    """Allow access only to users with 'staff' role"""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'staff'


class IsOwnerOrStaff(permissions.BasePermission):
    """
    Allow access to object owner (student) or clinic staff
    Students can only access their own records
    """
    
    def has_object_permission(self, request, view, obj):
        # Staff can access all records
        if request.user.role == 'staff':
            return True
        
        # Students can only access their own records
        if request.user.role == 'student':
            # Check if object has 'student' attribute
            if hasattr(obj, 'student'):
                return obj.student == request.user
            # Check if object is the user themselves
            if hasattr(obj, 'school_id'):
                return obj == request.user
        
        return False


class CanModifyProfile(permissions.BasePermission):
    """
    Students can modify only: name, department, cpsu_address
    Staff cannot modify student profiles
    Immutable fields: school_id, role
    """
    
    def has_object_permission(self, request, view, obj):
        # Can't modify other users' profiles
        if obj != request.user:
            return False
        
        # Check for attempts to modify immutable fields
        if request.method in ['PUT', 'PATCH']:
            immutable_fields = {'school_id', 'role'}
            attempted_changes = set(request.data.keys())
            
            if immutable_fields.intersection(attempted_changes):
                return False
        
        return True


class HasDataConsent(permissions.BasePermission):
    """
    Check if user has given consent for health data storage
    Required for symptom submission and AI features
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Staff always have implicit consent
        if request.user.role == 'staff':
            return True
        
        # Students must explicitly consent
        return request.user.data_consent_given
    
    message = "You must provide data consent before using this feature"
