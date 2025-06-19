from rest_framework import permissions

class IsStaffUser(permissions.BasePermission):
    """
    Allows access only to staff users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class IsAdminUser(permissions.BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

class IsOwnerOrStaff(permissions.BasePermission):
    """
    Allows access to object owners or staff users.
    """
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff