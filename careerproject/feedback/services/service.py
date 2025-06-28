from ..models import Feedback
from ..interfaces import IService
from ..exceptions import FeedbackServiceException

class FeedbackService(IService):
    @staticmethod
    def create_feedback(user, validated_data):
        try:
            return Feedback.objects.create(user=user, **validated_data)
        except Exception as e:
            raise FeedbackServiceException(f"Failed to create feedback: {str(e)}")

    @staticmethod
    def update_feedback(feedback, validated_data):
        try:
            for attr, value in validated_data.items():
                setattr(feedback, attr, value)
            feedback.save()
            return feedback
        except Exception as e:
            raise FeedbackServiceException(f"Failed to update feedback: {str(e)}")

    @staticmethod
    def delete_feedback(feedback):
        try:
            feedback.delete()
            return True
        except Exception as e:
            raise FeedbackServiceException(f"Failed to delete feedback: {str(e)}")