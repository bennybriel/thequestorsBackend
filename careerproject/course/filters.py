from django_filters import rest_framework as filters
from .models import Course, UTMERequirement

class CourseFilter(filters.FilterSet):
    school = filters.NumberFilter(field_name='school__id')
    school_name = filters.CharFilter(field_name='school__name', lookup_expr='icontains')
    name = filters.CharFilter(lookup_expr='icontains')
    status = filters.ChoiceFilter(choices=Course.STATUS_CHOICES)
    
    class Meta:
        model = Course
        fields = {
            'school': ['exact'],
            'school__name': ['exact', 'icontains'],
            'name': ['exact', 'icontains'],
            'status': ['exact'],
        }

class UTMERequirementFilter(filters.FilterSet):
    school = filters.NumberFilter(field_name='school__id')
    course = filters.NumberFilter(field_name='course__id')
    subject = filters.NumberFilter(field_name='subject__id')
    required_status = filters.CharFilter(field_name='required_status')
    status = filters.CharFilter(field_name='status')

    class Meta:
        model = UTMERequirement
        fields = ['school', 'course', 'subject', 'required_status', 'status']