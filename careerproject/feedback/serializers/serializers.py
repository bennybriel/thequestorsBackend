from rest_framework import serializers
from ..models import Feedback

class FeedbackCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['rating', 'comment', 'is_public']  # Only include fields that can be set by user
        extra_kwargs = {
            'rating': {'required': True},
            'comment': {'required': False, 'allow_blank': True},
            'is_public': {'required': False, 'default': True}
        }

    class Meta:
        model = Feedback
        fields = [
            'id', 'user', 'rating', 'rating_display',
            'comment', 'created_at', 'updated_at', 'is_public'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'user', 'rating_display']

    def get_rating_display(self, obj):
        # Handle case when obj is a dictionary (during create)
        if isinstance(obj, dict):
            return dict(Feedback.RATING_CHOICES).get(obj.get('rating'), '')
        return obj.rating_display
