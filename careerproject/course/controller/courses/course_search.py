from django.db.models import Prefetch
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Prefetch
from ...models import Course, UTMERequirement, OLevelRequirement

class SearchCoursesView(APIView):
    permission_classes = []
    def get(self, request):
        query = request.GET.get('q', '').strip()
        
        if not query:
            return Response(
                {'error': 'Please enter a search term'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create a comprehensive search query across multiple fields
        search_query = (
            Q(name__icontains=query) 
            #Q(school__name__icontains=query) |
            #Q(utme_requirements__subject__name__icontains=query) |
            #Q(olevel_requirements__subject__name__icontains=query)
        )
        
        # Get distinct courses matching the search
        courses = Course.objects.filter(
            search_query,
            status='active'
        ).distinct().select_related('school').prefetch_related(
            Prefetch('utme_requirements', 
                   queryset=UTMERequirement.objects.filter(status='1').select_related('subject'),
                   to_attr='active_utme_reqs'),
            Prefetch('olevel_requirements',
                   queryset=OLevelRequirement.objects.filter(status='1').select_related('subject'),
                   to_attr='active_olevel_reqs')
        )
        
        print(courses)
        results = []
        
        for course in courses:
            # Get matching UTME requirements (filtered by search term if applicable)
            utme_requirements = [{
                'subject_id': req.subject.id,
                'subject': req.subject.name,
                'status': req.get_required_status_display(),
                'status_code': req.required_status
            } for req in getattr(course, 'active_utme_reqs', []) 
              if query.lower() in req.subject.name.lower() or not query] or None
            
            # Get matching O'Level requirements (filtered by search term if applicable)
            olevel_requirements = [{
                'subject_id': req.subject.id,
                'subject': req.subject.name,
                'status': req.get_required_status_display(),
                'status_code': req.required_status
            } for req in getattr(course, 'active_olevel_reqs', []) 
              if query.lower() in req.subject.name.lower() or not query] or None
            
            results.append({
                'school_id': course.school.id,
                'school_name': course.school.name,
                'school_website': course.school.website,
                'course_id': course.id,
                'course_name': course.name,
                'utme_requirements': utme_requirements,
                'olevel_requirements': olevel_requirements,
                'matching_score': self._calculate_matching_score(course, query)
            })
        
        # Sort by matching score (higher scores first)
        results.sort(key=lambda x: x['matching_score'], reverse=True)
        
        return Response({
            'count': len(results),
            'results': results
        })
    
    def _calculate_matching_score(self, course, query):
        """Calculate how well the course matches the search query"""
        score = 0
        query = query.lower()
        
        # Course name match
        if query in course.name.lower():
            score += 3
        elif any(word in course.name.lower() for word in query.split()):
            score += 2
            
        # School name match
        if query in course.school.name.lower():
            score += 2
            
        # Subject matches in requirements
        utme_subjects = [req.subject.name.lower() 
                        for req in getattr(course, 'active_utme_reqs', [])]
        olevel_subjects = [req.subject.name.lower() 
                         for req in getattr(course, 'active_olevel_reqs', [])]
        
        if query in utme_subjects or query in olevel_subjects:
            score += 1
        elif any(word in utme_subjects + olevel_subjects for word in query.split()):
            score += 0.5
            
        return score
    
class AdvancedSearchCoursesView(APIView):
    def get(self, request):
        course_query = request.GET.get('course', '').strip()
        school_query = request.GET.get('school', '').strip()
        subject_query = request.GET.get('subject', '').strip()
        
        # Base queryset
        courses = Course.objects.filter(status='active').select_related('school')
        
        # Apply filters
        if course_query:
            courses = courses.filter(name__icontains=course_query)
        if school_query:
            courses = courses.filter(school__name__icontains=school_query)
        
        # Subject filter optimization
        if subject_query:
            # Single query to get both UTME and O'Level courses with the subject
            subject_courses = Course.objects.filter(
                Q(utme_requirements__subject__name__icontains=subject_query, 
                  utme_requirements__status='active') |
                Q(olevel_requirements__subject__name__icontains=subject_query,
                  olevel_requirements__status='active'),
                status='active'
            ).distinct()
            
            if course_query or school_query:
                courses = courses.filter(id__in=subject_courses.values_list('id', flat=True))
            else:
                courses = subject_courses
        
        # Prefetch related data for performance
        courses = courses.prefetch_related(
            'utme_requirements__subject',
            'olevel_requirements__subject'
        )
        
        results = []
        
        for course in courses:
            utme_requirements = [{
                'subject': req.subject.name,
                'status': req.get_required_status_display()
            } for req in course.utme_requirements.filter(status='active')]
            
            olevel_requirements = [{
                'subject': req.subject.name,
                'status': req.get_required_status_display()
            } for req in course.olevel_requirements.filter(status='active')]
            
            results.append({
                'school_id': course.school.id,
                'school': course.school.name,
                'course_id': course.id,
                'course': course.name,
                'utme_requirements': utme_requirements,
                'olevel_requirements': olevel_requirements,
                'school_website': course.school.website
            })
        
        return Response({
            'count': len(results),
            'results': results
        })




class CourseRequirementsView(APIView):
    permission_classes = []
    """
    API endpoint to get UTME and O'Level requirements for a specific course
    """
    def get(self, request, course_id):
        try:
            # Get the course with prefetched requirements
            course = Course.objects.filter(
                id=course_id,
                status='active'
            ).prefetch_related(
                Prefetch('utme_requirements',
                       queryset=UTMERequirement.objects.filter(status='1').select_related('subject'),
                       to_attr='active_utme_reqs'),
                Prefetch('olevel_requirements',
                       queryset=OLevelRequirement.objects.filter(status='1').select_related('subject'),
                       to_attr='active_olevel_reqs')
            ).get()
            
            # Prepare response data
            data = {
                'course_id': course.id,
                'course_name': course.name,
                'school_id': course.school.id,
                'school_name': course.school.name,
                'utme_requirements': [{
                    'id':req.id,
                    'subject_id': req.subject.id,
                    'subject': req.subject.name,
                    'status': req.get_required_status_display(),
                    'status_code': req.required_status
                } for req in course.active_utme_reqs],
                'olevel_requirements': [{
                    'id':req.id,
                    'subject_id': req.subject.id,
                    'subject': req.subject.name,
                    'status': req.get_required_status_display(),
                    'status_code': req.required_status
                } for req in course.active_olevel_reqs]
            }
            
            return Response(data)
            
        except Course.DoesNotExist:
            return Response(
                {'error': 'Course not found or inactive'},
                status=status.HTTP_404_NOT_FOUND
            )