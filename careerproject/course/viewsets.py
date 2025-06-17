from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Course
from .serializers import CourseSerializer
from .services.course_services import CourseService
from .permissions import IsCourseActive, IsSchoolActive
from .filters import CourseFilter
from django_filters.rest_framework import DjangoFilterBackend
from .exceptions import (  # Add this import
    DuplicateCourseException,
    CourseAPIException,
    InactiveSchoolException
)
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CourseFilter
    permission_classes = [IsSchoolActive]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [*super().get_permissions(), IsCourseActive()]
        return super().get_permissions()
    
    def get_queryset(self):
        return self.queryset.filter(status=Course.ACTIVE).select_related('school')
    
    def perform_create(self, serializer):
        service = CourseService()
        course = service.create_course(
            name=serializer.validated_data['name'],
            school_id=serializer.validated_data.get('school_id')  # Using .get() for safety
        )
        serializer.instance = course
    
    def perform_update(self, serializer):
        service = CourseService()
        course = service.update_course(
            course_id=self.get_object().id,
            **serializer.validated_data
        )
        serializer.instance = course
    
    def perform_destroy(self, instance):
        service = CourseService()
        service.delete_course(course_id=instance.id)
    
    @action(detail=False, methods=['get'])
    def inactive(self, request):
        queryset = Course.objects.filter(status=Course.INACTIVE)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def handle_exception(self, exc):
        if isinstance(exc, (DuplicateCourseException, InactiveSchoolException)):
            return Response(
                {'detail': exc.detail},
                status=exc.status_code
            )
        return super().handle_exception(exc)