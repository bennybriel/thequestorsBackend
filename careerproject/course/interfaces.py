from abc import ABC, abstractmethod
from typing import Optional
from .models import Course

class ICourseRepository(ABC):
    @abstractmethod
    def get_by_id(self, course_id: int) -> Optional[Course]:
        pass
    
    @abstractmethod
    def get_all_active(self):
        pass
    
    @abstractmethod
    def create(self, name: str, school_id: int) -> Course:
        pass
    
    @abstractmethod
    def update(self, course_id: int, **kwargs) -> Course:
        pass
    
    @abstractmethod
    def deactivate(self, course_id: int) -> Course:
        pass

class ICourseService(ABC):
    @abstractmethod
    def get_course(self, course_id: int) -> Course:
        pass
    
    @abstractmethod
    def list_courses(self, filters: dict = None):
        pass
    
    @abstractmethod
    def create_course(self, name: str, school_id: int) -> Course:
        pass
    
    @abstractmethod
    def update_course(self, course_id: int, **kwargs) -> Course:
        pass
    
    @abstractmethod
    def delete_course(self, course_id: int) -> None:
        pass