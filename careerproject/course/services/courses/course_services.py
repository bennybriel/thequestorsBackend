from typing import Optional
from ...interfaces import ICourseService
from ...repositories import CourseRepository
from ...models import Course, School
from ...exceptions import CourseAPIException
from ...exceptions import DuplicateCourseException  # Add this import

class CourseService(ICourseService):
    def __init__(self, repository: CourseRepository = None):
        self.repository = repository or CourseRepository()
    
    def get_course(self, course_id: int) -> Course:
        course = self.repository.get_by_id(course_id)
        if not course:
            raise CourseAPIException(detail="Course not found", status_code=404)
        return course
    
    def list_courses(self, filters: dict = None):
        queryset = self.repository.get_all_active()
        # Apply filters if needed
        if filters:
            pass  # Filter implementation would go here
        return queryset
    
    # def create_course(self, name: str, school_id: int) -> Course:
    #     if not school_id:
    #         raise CourseAPIException(detail="school_id is required", status_code=400)
    #     # Check for existing active course
    #     school_guid = School.get(id=school_guid).first()
    #     if Course.objects.filter(
    #         name=name,
    #         school_id=school_id,
    #         guid =school_guid.guid,
    #         status=Course.ACTIVE
    #     ).exists():
    #         raise CourseAPIException(
    #             detail="Course already exists in this school",
    #             status_code=status.HTTP_409_CONFLICT
    #         )
    #     return self.repository.create(name, school_id)
    def create_course(self, name: str, school_id: int) -> Course:
        # Input validation
        if not school_id:
            raise CourseAPIException(detail="school_id is required", status_code=400)
        
        if not name or not isinstance(name, str):
            raise CourseAPIException(detail="Valid course name is required", status_code=400)
        
        # Get school (with existence check)
        try:
            school = School.objects.get(id=school_id)
        except School.DoesNotExist:
            raise CourseAPIException(detail="School not found", status_code=404)
        
        # Check for existing active course (case-insensitive)
        if Course.objects.filter(
            name__iexact=name,
            school_id=school_id,
            guid=school.guid,
            status=Course.ACTIVE
        ).exists():
            raise CourseAPIException(
                detail=f"Active course '{name}' already exists in this school",
                status_code=status.HTTP_409_CONFLICT
            )
        
        # Create the course
        try:
            return self.repository.create(name, school_id)
        except Exception as e:
            raise CourseAPIException(
                detail=f"Failed to create course: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    def update_course(self, course_id: int, **kwargs) -> Course:
        course = self.repository.update(course_id, **kwargs)
        if not course:
            raise CourseAPIException(detail="Course not found", status_code=404)
        return course
    
    def delete_course(self, course_id: int) -> None:
        course = self.repository.deactivate(course_id)
        if not course:
            raise CourseAPIException(detail="Course not found", status_code=404)