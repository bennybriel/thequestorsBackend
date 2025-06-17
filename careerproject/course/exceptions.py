from rest_framework.exceptions import APIException
from rest_framework import status

class CourseAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Course service error occurred'
    default_code = 'course_service_error'

class InactiveSchoolException(CourseAPIException):
    default_detail = 'Cannot perform operation on inactive school'
    default_code = 'inactive_school'

class DuplicateCourseException(CourseAPIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'Course with this name already exists in the school'
    default_code = 'duplicate_course'
    
class OLevelRequirementServiceException(Exception):
    """Base exception for OLevelRequirement service layer"""
    pass