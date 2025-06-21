from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from ...models import School, Course
from ...serializers.schools.serial_schools import SchoolSerializer,SchoolCourseListSerializer
from ...serializers.courses.serial_courses import CourseSerializer
from django.shortcuts import get_object_or_404

class SchoolListCreateView(generics.ListCreateAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    lookup_field = 'guid'

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.query_params.get('status')
        search = self.request.query_params.get('search')
        
        if status:
            queryset = queryset.filter(status=status)
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        return queryset

class SchoolRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    lookup_field = 'guid'

class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        school_guid = self.request.query_params.get('school_guid')
        status = self.request.query_params.get('status')
        search = self.request.query_params.get('search')
        
        if school_guid:
            queryset = queryset.filter(school__guid=school_guid)
        if status:
            queryset = queryset.filter(status=status)
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        return queryset

class CourseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'guid'

class SchoolCoursesListView(generics.ListAPIView):
    serializer_class = SchoolCourseListSerializer

    def get_queryset(self):
        school_guid = self.kwargs['school_guid']
        school = get_object_or_404(School, guid=school_guid)
        return Course.objects.filter(school=school)