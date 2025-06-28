from rest_framework import generics
from ..models.education import EducationPath, University, UniversityCareerPath
from .base import BaseListView, BaseDetailView
from ..serializers.education import (
    EducationPathSerializer,
    UniversitySerializer,
    UniversityCareerPathSerializer
)

class UniversityListView(BaseListView):
    serializer_class = UniversitySerializer
    model = University
    permission_classes = []  # Public access

class UniversityDetailView(BaseDetailView):
    serializer_class = UniversitySerializer
    model = University
    permission_classes = []  # Public access

class EducationPathListView(BaseListView):
    serializer_class = EducationPathSerializer
    model = EducationPath
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if 'career_path' in self.request.query_params:
            queryset = queryset.filter(
                career_path_id=self.request.query_params['career_path'])
        return queryset

class EducationPathDetailView(BaseDetailView):
    serializer_class = EducationPathSerializer
    model = EducationPath

class UniversityCareerPathListView(BaseListView):
    serializer_class = UniversityCareerPathSerializer
    model = UniversityCareerPath
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if 'career_path' in self.request.query_params:
            queryset = queryset.filter(
                career_path_id=self.request.query_params['career_path'])
        return queryset.order_by('-strength_rating')

class UniversityCareerPathDetailView(BaseDetailView):
    serializer_class = UniversityCareerPathSerializer
    model = UniversityCareerPath