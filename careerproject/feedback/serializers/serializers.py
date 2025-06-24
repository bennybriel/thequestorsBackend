from rest_framework import serializers
from ..models import Feedback
from ..interfaces import ISerializerValidator

class FeedbackSerializer(serializers.ModelSerializer, ISerializerValidator):
    rating_display = serializers.SerializerMethodField(read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Feedback
        fields = [
            'id', 'user', 'rating', 'rating_display', 
            'comment', 'created_at', 'updated_at', 'is_public'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']

    def get_rating_display(self, obj):
        return obj.rating_display

    def validate(self, data):
        """Validate serializer data"""
        if len(data.get('comment', '')) > 1000:
            raise serializers.ValidationError("Comment cannot exceed 1000 characters.")
        return data

class FeedbackCreateSerializer(FeedbackSerializer):
    """Serializer for creating feedback with additional validation"""
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value