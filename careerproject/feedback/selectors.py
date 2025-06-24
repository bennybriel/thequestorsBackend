from .models import Feedback
from .interfaces import ISelector

class FeedbackSelector(ISelector):
    @staticmethod
    def get_user_feedbacks(user):
        return Feedback.objects.filter(user=user).order_by('-created_at')

    @staticmethod
    def get_public_feedbacks():
        return Feedback.objects.filter(is_public=True).order_by('-created_at')

    @staticmethod
    def get_feedback_by_id(feedback_id):
        try:
            return Feedback.objects.get(id=feedback_id)
        except Feedback.DoesNotExist:
            return None

    @staticmethod
    def get_average_rating():
        from django.db.models import Avg
        result = Feedback.objects.filter(is_public=True).aggregate(Avg('rating'))
        return result['rating__avg'] or 0