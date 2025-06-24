from rest_framework import permissions
from .interfaces import IPermission

class IsFeedbackOwnerOrReadOnly(permissions.BasePermission, IPermission):
    """
    Custom permission to only allow owners of feedback to edit it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

class IsAdminOrPublicReadOnly(permissions.BasePermission, IPermission):
    """
    Allows read-only access to public feedbacks, full access to admins.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff