# urls.py
from .views import CourseSearchView
from .controller.upload_subject import SubjectUploadView, SubjectCSVUploadView
from .controller.upload_school import SchoolUploadView, SchoolCSVUploadView
from .controller.upload_course import CourseCSVUploadView
from .controller.upload_utme_requirement import UTMERequirementCSVUploadView
from .controller.upload_olevel_requirement import OLevelRequirementCSVUploadView
from .controller.course_search import SearchCoursesView, AdvancedSearchCoursesView,CourseRequirementsView
from .viewers.school_viewset import SchoolViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import CourseViewSet
from .controller.olevel_requirements import OLevelRequirementViewSet
from .controller.utme_requirements import (
    UTMERequirementListCreateView,
    UTMERequirementRetrieveUpdateDestroyView
)

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'schools', SchoolViewSet, basename='school')
router.register(r'olevel', OLevelRequirementViewSet, basename='olevel-requirement')


urlpatterns = [
    path('', include(router.urls)),
    path('olevel/', include(router.urls)),
    path('courses/', include(router.urls)),
    path('courses/search/', CourseSearchView.as_view(), name='course-search'),
    path('subjects/upload/', SubjectCSVUploadView.as_view(), name='subject-upload'),
    path('subjects/', SubjectUploadView.as_view(), name='subject_upload'),
    path('schools/upload/', SchoolCSVUploadView.as_view(), name='school-upload'),
    path('courses/upload/', CourseCSVUploadView.as_view(), name='course-upload'),
    path('utme-requirements/upload/', UTMERequirementCSVUploadView.as_view(), name='utme-requirement-csv-upload'),
    path('olevel-requirements/upload/', OLevelRequirementCSVUploadView.as_view(), name='olevel-requirement-csv-upload'),
    path('search/', SearchCoursesView.as_view(), name='search_courses'),
    path('search/advanced/', AdvancedSearchCoursesView.as_view(), name='search_courses_advanced'),
    path('course/<int:course_id>/requirements/', CourseRequirementsView.as_view(), name='course-requirements'),
    path('utme/', UTMERequirementListCreateView.as_view(), name='utme-requirement-list-create'),
    path('utme/<int:pk>/', UTMERequirementRetrieveUpdateDestroyView.as_view(), name='utme-requirement-retrieve-update-destroy'),
   
]