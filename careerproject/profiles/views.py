from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile
from .serializers import UserProfileSerializer, ProfileUpdateSerializer

class UserProfileDetailView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

class ProfileUpdateView(generics.UpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = ProfileUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

    def perform_update(self, serializer):
        # Auto-classify hobbies if they're updated
        if 'hobbies' in serializer.validated_data:
            hobbies = serializer.validated_data['hobbies']
            # Add your hobby classification logic here
            # Example: categories = classify_hobbies(hobbies)
            categories = ['TECH', 'READ']  # Placeholder
            serializer.save(hobby_categories=categories)
        else:
            serializer.save()


