from rest_framework import serializers
from .models import MentorshipConnection, MentorshipMessage
from users.serializers import UserSerializer
from careers.serializers import CareerSerializer

class MentorshipMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = MentorshipMessage
        fields = '__all__'

class MentorshipConnectionSerializer(serializers.ModelSerializer):
    mentor = UserSerializer(read_only=True)
    mentee = UserSerializer(read_only=True)
    career = CareerSerializer(read_only=True)
    messages = MentorshipMessageSerializer(many=True, read_only=True)

    class Meta:
        model = MentorshipConnection
        fields = '__all__'

class MentorshipRequestSerializer(serializers.Serializer):
    mentor_id = serializers.IntegerField()
    career_id = serializers.IntegerField(required=False)
    goals = serializers.CharField(required=False)