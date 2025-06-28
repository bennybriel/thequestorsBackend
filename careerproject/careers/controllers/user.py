from rest_framework import generics
from ..models.user import UserProfile
from .base import BaseListView, BaseDetailView
from ..serializers.user import UserProfileSerializer
from rest_framework import generics, permissions

class UserProfileListView(BaseListView):
    serializer_class = UserProfileSerializer
    model = UserProfile
    
    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

class UserProfileDetailView(BaseDetailView):
    serializer_class = UserProfileSerializer
    model = UserProfile
    
    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)




class UserProfileListView(BaseListView):
    serializer_class = UserProfileSerializer
    model = UserProfile
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserProfileDetailView(BaseDetailView):
    serializer_class = UserProfileSerializer
    model = UserProfile
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)