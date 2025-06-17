# services/base_service.py
from abc import ABC, abstractmethod
from typing import Type, TypeVar, Generic, Optional
from django.db.models import Model

T = TypeVar('T', bound=Model)

class BaseService(Generic[T], ABC):
    model_class: Type[T]

    @abstractmethod
    def get_all(self, **filters):
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[T]:
        pass

    @abstractmethod
    def create(self, data: dict) -> T:
        pass

    @abstractmethod
    def update(self, id: int, data: dict) -> T:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass