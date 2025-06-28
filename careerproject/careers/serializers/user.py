from rest_framework import serializers
from ..models.user import UserProfile
from rest_framework import serializers
from ..models.user import UserProfile
from django.contrib.auth.models import User
from .base import DynamicFieldsModelSerializer
from ..models.user import UserProfile

class UserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        extra_kwargs = {
            'email': {'required': True},
            'username': {'read_only': True}
        }

class UserProfileSerializer(DynamicFieldsModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }

    def to_representation(self, instance):
        """
        Custom representation to include nested user data
        """
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data
        return representation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        extra_kwargs = {
            'email': {'required': True}
        }

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }