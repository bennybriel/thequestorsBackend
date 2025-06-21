# views.py
from rest_framework import generics, response, status
from rest_framework.views import APIView
from django.db.models import Q
from .models import School, Course, Subject, UTMERequirement, OLevelRequirement
from .serializers.courses.serial_courses import CourseSerializer, CourseRequirementsSerializer

class CourseSearchView(generics.ListAPIView):
    permission_classes = []
    serializer_class = CourseSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return Course.objects.filter(
            Q(name__icontains=query) |
            Q(school__name__icontains=query),
            status='active'
        ).select_related('school')

class CourseRequirementsView(APIView):
    permission_classes = []
    def get(self, request, school_id, course_id):
        try:
            school = School.objects.get(id=school_id, status='active')
            course = Course.objects.get(id=course_id, school=school, status='active')

            utme_reqs = UTMERequirement.objects.filter(
                school=school,
                course=course,
                status='active'
            ).select_related('subject')

            olevel_reqs = OLevelRequirement.objects.filter(
                school=school,
                course=course,
                status='active'
            ).select_related('subject')

            serializer = CourseRequirementsSerializer({
                'school': school,
                'course': course,
                'utme_requirements': utme_reqs,
                'olevel_requirements': olevel_reqs
            })

            #print(serializer.data)
            return response.Response(serializer.data)

        except School.DoesNotExist:
            return response.Response(
                {'error': 'School not found or inactive'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Course.DoesNotExist:
            return response.Response(
                {'error': 'Course not found or inactive for this school'},
                status=status.HTTP_404_NOT_FOUND
            )