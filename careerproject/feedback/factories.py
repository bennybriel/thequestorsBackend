from .models import Feedback
from .services.service import FeedbackService
from .selectors import FeedbackSelector
from .exceptions import FeedbackNotFoundException

class FeedbackFactory:
    @staticmethod
    def create_service():
        return FeedbackService()

    @staticmethod
    def create_selector():
        return FeedbackSelector()

    @staticmethod
    def get_feedback_or_raise(feedback_id):
        selector = FeedbackFactory.create_selector()
        feedback = selector.get_feedback_by_id(feedback_id)
        if not feedback:
            raise FeedbackNotFoundException(f"Feedback with id {feedback_id} not found")
        return feedback