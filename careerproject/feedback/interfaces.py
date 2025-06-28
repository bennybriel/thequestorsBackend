from abc import ABC, abstractmethod
from rest_framework.serializers import Serializer

class ISerializerValidator(ABC):
    @abstractmethod
    def validate(self, data):
        pass

class IPermission(ABC):
    @abstractmethod
    def has_permission(self, request, view):
        pass

    @abstractmethod
    def has_object_permission(self, request, view, obj):
        pass

class IService(ABC):
    @staticmethod
    @abstractmethod
    def create_feedback(user, validated_data):
        pass

    @staticmethod
    @abstractmethod
    def update_feedback(feedback, validated_data):
        pass

    @staticmethod
    @abstractmethod
    def delete_feedback(feedback):
        pass

class ISelector(ABC):
    @staticmethod
    @abstractmethod
    def get_user_feedbacks(user):
        pass

    @staticmethod
    @abstractmethod
    def get_public_feedbacks():
        pass

    @staticmethod
    @abstractmethod
    def get_feedback_by_id(feedback_id):
        pass