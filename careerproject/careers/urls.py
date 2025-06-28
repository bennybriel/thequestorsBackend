from django.urls import path
from .controllers.user import UserProfileListView, UserProfileDetailView
from .controllers.career import (CareerSearchView, CareerPlanView, CareerPlanPDFView ,CareerPathListView, 
                                 CareerPathDetailView,ProfessionalQualificationListView, 
                                 ProfessionalQualificationDetailView)

from .controllers.education import (
    UniversityListView, UniversityDetailView,
    EducationPathListView, EducationPathDetailView,
    UniversityCareerPathListView, UniversityCareerPathDetailView
)

urlpatterns = [
    # User endpoints
    path('user/profile/', UserProfileListView.as_view(), name='user-profile-list'),
    path('user/profile/<int:pk>/', UserProfileDetailView.as_view(), name='user-profile-detail'),
    # Career endpoints
    path('careers/', CareerPathListView.as_view(), name='career-path-list'),
    path('careers/<int:pk>/', CareerPathDetailView.as_view(), name='career-path-detail'),
    path('qualifications/', ProfessionalQualificationListView.as_view(), name='qualification-list'),
    path('qualifications/<int:pk>/', ProfessionalQualificationDetailView.as_view(), name='qualification-detail'),
    # Education endpoints
    path('universities/', UniversityListView.as_view(), name='university-list'),
    path('universities/<int:pk>/', UniversityDetailView.as_view(), name='university-detail'),
    path('education-paths/', EducationPathListView.as_view(), name='education-path-list'),
    path('education-paths/<int:pk>/', EducationPathDetailView.as_view(), name='education-path-detail'),
    path('university-careers/', UniversityCareerPathListView.as_view(), name='university-career-list'),
    path('university-careers/<int:pk>/', UniversityCareerPathDetailView.as_view(), name='university-career-detail'),
    #search
    path('search/', CareerSearchView.as_view(), name='career-search'),
    path('plans/<int:career_id>/', CareerPlanView.as_view(), name='career-plan'),
    path('plans/<int:career_id>/pdf/', CareerPlanPDFView.as_view(), name='career-plan-pdf'),
]