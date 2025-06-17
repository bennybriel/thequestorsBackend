from django.core.exceptions import ObjectDoesNotExist
from typing import Optional
from .models import Course, School
from .interfaces import ICourseRepository
from .exceptions import InactiveSchoolException

class CourseRepository(ICourseRepository):
    def get_by_id(self, course_id: int) -> Optional[Course]:
        try:
            return Course.objects.get(pk=course_id)
        except ObjectDoesNotExist:
            return None
    
    def get_all_active(self):
        return Course.objects.filter(status=Course.ACTIVE).select_related('school')
    
    def create(self, name: str, school_id: int) -> Course:
        school = School.objects.get(pk=school_id)
        if school.status != School.ACTIVE:
            raise InactiveSchoolException()
        return Course.objects.create(name=name, school=school)
    
    def update(self, course_id: int, **kwargs) -> Course:
        Course.objects.filter(pk=course_id).update(**kwargs)
        return self.get_by_id(course_id)
    
    def deactivate(self, course_id: int) -> Course:
        course = self.get_by_id(course_id)
        if course:
            course.status = Course.INACTIVE
            course.save()
        return course