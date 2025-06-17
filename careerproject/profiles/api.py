from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile
from .serializers import ProfileSerializer
from .services import HobbyClassifier

class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

    def perform_update(self, serializer):
        instance = serializer.save()

        # Automatically classify hobbies
        if 'hobbies' in serializer.validated_data:
            classifier = HobbyClassifier()
            categories = classifier.classify_hobbies(instance.hobbies)
            instance.hobby_categories = categories
            instance.save()