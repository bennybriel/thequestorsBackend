from rest_framework import serializers
from .models import UserProfile
from careers.serializers import CareerSerializer
from users.serializers import UserSerializer

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    current_career = CareerSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'hobbies',
            'happy_activities',
            'personal_vision',
            'personality_type',
            'career_goals',
            'current_career',
            'skills'
        ]