from .models import OLevelRequirement, UTMERequirement
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
    
class UTMERequirementSelector:
    @staticmethod
    def list_utme_requirements(filters):
        queryset = UTMERequirement.objects.select_related(
            'school', 'course', 'subject'
        ).filter(
            status=UTMERequirement.ACTIVE,
            course__status=Course.ACTIVE,
            subject__status=Subject.ACTIVE
        )
        
        if filters.get('school_id'):
            queryset = queryset.filter(school_id=filters['school_id'])
        if filters.get('course_id'):
            queryset = queryset.filter(course_id=filters['course_id'])
        if filters.get('subject_id'):
            queryset = queryset.filter(subject_id=filters['subject_id'])
        if filters.get('required_status'):
            queryset = queryset.filter(required_status=filters['required_status'])
        if filters.get('status'):
            queryset = queryset.filter(status=filters['status'])
        if filters.get('search'):
            queryset = queryset.filter(
                Q(school__name__icontains=filters['search']) |
                Q(course__name__icontains=filters['search']) |
                Q(subject__name__icontains=filters['search'])
            )
            
        return queryset.order_by('school__name', 'course__name', 'subject__name')