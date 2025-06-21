# urls.py
from .views import CourseSearchView
from .controller.subjects.upload_subject import SubjectUploadView, SubjectCSVUploadView
from .controller.schools.upload_school import SchoolUploadView, SchoolCSVUploadView
from .controller.courses.upload_course import CourseCSVUploadView
from .controller.utme.upload_utme_requirement import UTMERequirementCSVUploadView
from .controller.olevels.upload_olevel_requirement import OLevelRequirementCSVUploadView
from .controller.courses.course_search import SearchCoursesView, AdvancedSearchCoursesView,CourseRequirementsView
from .viewers.school_viewset import SchoolViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import CourseViewSet
from .controller.olevels.olevel_requirements import OLevelRequirementViewSet
from .controller.schools.school_guid import SchoolGuidUpdateView
from .controller.utme.utme_requirements import (
    UTMERequirementListCreateView,
    UTMERequirementRetrieveUpdateDestroyView
)

from .controller.schools.schools import (
    SchoolListCreateView,
    SchoolRetrieveUpdateDestroyView,
    CourseListCreateView,
    CourseRetrieveUpdateDestroyView,
    SchoolCoursesListView
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
    #path('subjects/', SubjectUploadView.as_view(), name='subject_upload'),
    path('schools/upload/', SchoolCSVUploadView.as_view(), name='school-upload'),
    path('courses/upload/', CourseCSVUploadView.as_view(), name='course-upload'),
    path('utme-requirements/upload/', UTMERequirementCSVUploadView.as_view(), name='utme-requirement-csv-upload'),
    path('olevel-requirements/upload/', OLevelRequirementCSVUploadView.as_view(), name='olevel-requirement-csv-upload'),
    path('search/', SearchCoursesView.as_view(), name='search_courses'),
    path('search/advanced/', AdvancedSearchCoursesView.as_view(), name='search_courses_advanced'),
    path('course/<int:course_id>/requirements/', CourseRequirementsView.as_view(), name='course-requirements'),
    path('utme/', UTMERequirementListCreateView.as_view(), name='utme-requirement-list-create'),
    path('utme/<int:pk>/', UTMERequirementRetrieveUpdateDestroyView.as_view(), name='utme-requirement-retrieve-update-destroy'),
    path('update-guids/', SchoolGuidUpdateView.as_view(), name='update-user-guids'),
    # Schools endpoints
    path('schools/', SchoolListCreateView.as_view(), name='school-list-create'),
    path('schools/<uuid:guid>/', SchoolRetrieveUpdateDestroyView.as_view(), name='school-retrieve-update-destroy'),
    path('schools/courses/<uuid:school_guid>/', SchoolCoursesListView.as_view(), name='school-courses-list'),
   
]