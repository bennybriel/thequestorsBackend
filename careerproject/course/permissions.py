from rest_framework.permissions import BasePermission
from .models import Course
from rest_framework import permissions

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user and request.user.is_staff
    
class IsCourseActive(BasePermission):
    message = "Cannot perform this action on inactive course"
    
    def has_object_permission(self, request, view, obj):
        return obj.status == Course.ACTIVE

class IsSchoolActive(BasePermission):
    message = "Cannot perform this action with inactive school"
    
    def has_permission(self, request, view):
        if request.method == 'POST':
            school_id = request.data.get('school_id')
            if school_id:
                from .models import School
                try:
                    school = School.objects.get(pk=school_id)
                    return school.status == School.ACTIVE
                except School.DoesNotExist:
                    return False
        return True
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class IsSchoolAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff or (hasattr(request.user, 'schooladmin') and request.user.schooladmin.school == obj.school)