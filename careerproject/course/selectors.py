from .models import OLevelRequirement
from django.db.models import Q

class OLevelRequirementSelector:
    @staticmethod
    def get_olevel_requirement(pk):
        try:
            return OLevelRequirement.objects.get(pk=pk)
        except OLevelRequirement.DoesNotExist:
            return None

    @staticmethod
    def list_olevel_requirements(filters=None):
        queryset = OLevelRequirement.objects.all()
        
        if not filters:
            return queryset
        
        if 'school_id' in filters:
            queryset = queryset.filter(school_id=filters['school_id'])
        if 'course_id' in filters:
            queryset = queryset.filter(course_id=filters['course_id'])
        if 'subject_id' in filters:
            queryset = queryset.filter(subject_id=filters['subject_id'])
        if 'required_status' in filters:
            queryset = queryset.filter(required_status=filters['required_status'])
        if 'status' in filters:
            queryset = queryset.filter(status=filters['status'])
        if 'search' in filters:
            queryset = queryset.filter(
                Q(course__name__icontains=filters['search']) |
                Q(subject__name__icontains=filters['search'])
            )
            
        return queryset