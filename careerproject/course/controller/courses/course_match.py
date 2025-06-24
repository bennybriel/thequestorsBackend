from django.db.models import Q, Exists, OuterRef
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ...models import Course, UTMERequirement, Subject

def check_required_subjects(course, subject_ids):
    """Check if course's required subjects are all present in subject_ids."""
    required_subjects = set(
        course.utme_requirements.filter(
            required_status='required'
        ).values_list('subject_id', flat=True)
    )
    return required_subjects.issubset(subject_ids)

def check_optional_subjects(course, subject_ids):
    """Check if at least one optional subject is present in subject_ids if required."""
    optional_subjects = course.utme_requirements.filter(
        required_status='not_required'
    ).values_list('subject_id', flat=True)
    if not optional_subjects:
        return True  # No optional subjects needed
    return any(subject_id in optional_subjects for subject_id in subject_ids)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def find_courses_with_requirements(request):
    """Find courses matching exactly 4 subject IDs."""
    # Expected payload: {"subject_ids": [17, 77, 26, 41]}
    subject_ids = request.data.get('subject_ids', [])
    
    # Validate input
    if not isinstance(subject_ids, list):
        return Response({'error': 'Subject IDs must be a list'}, status=400)
    
    try:
        subject_ids = list({int(id) for id in subject_ids})
    except (ValueError, TypeError):
        return Response({'error': 'Invalid subject IDs'}, status=400)
    
    # Ensure exactly 4 subjects
    if len(subject_ids) != 4:
        return Response({'error': 'Exactly 4 subject IDs must be provided'}, status=400)
    
    # Find courses with active status
    base_query = Course.objects.filter(status='active')
    
    # Filter courses where all required subjects are in subject_ids
    results = []
    for course in base_query.distinct():
        # Check required subjects
        if not check_required_subjects(course, subject_ids):
            continue
            
        # Check optional subjects (if any)
        if not check_optional_subjects(course, subject_ids):
            continue
            
        requirements = (
            course.utme_requirements
            .select_related('subject')
            .order_by('-required_status')
        )
        
        # Categorize requirements
        required_matched = []
        optional_matched = []
        other_requirements = []
        
        for req in requirements:
            subj_data = {
                'id': req.subject.id,
                'name': req.subject.name,
                'status': req.required_status
            }
            
            if req.subject.id in subject_ids and req.required_status == 'required':
                required_matched.append(subj_data)
            elif req.subject.id in subject_ids and req.required_status == 'not_required':
                optional_matched.append(subj_data)
            elif req.required_status == 'required':
                other_requirements.append(subj_data)
        
        # Verify criteria: all required subjects and at least one optional (if needed)
        meets_criteria = len(required_matched) == course.utme_requirements.filter(
            required_status='required'
        ).count()
        
        if meets_criteria:
            results.append({
                'course_id': course.id,
                'course_name': course.name,
                'school_id':course.school.id,
                'school_name': course.school.name,
                'school_website': course.school.website
                ,
                'required_matched': sorted(required_matched, key=lambda x: x['id']),
                'optional_matched': sorted(optional_matched, key=lambda x: x['id']),
                'other_required': sorted(other_requirements, key=lambda x: x['id']),
                'criteria_met': True
            })
    
    return Response({
        'meta': {
            'subject_ids': subject_ids,
            'total_courses': len(results)
        },
        'results': results
    })