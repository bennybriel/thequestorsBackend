from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Feedback
from ..serializers.serializers import  FeedbackCreateSerializer

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    permission_classes = [IsAuthenticated]  # Require authentication
    
    def get_serializer_class(self):
        if self.action == 'create':
            return FeedbackCreateSerializer
        return FeedbackCreateSerializer

    def perform_create(self, serializer):
        # Automatically assign the current user to the feedback
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Return the full created object with rating_display
        instance = serializer.instance
        response_serializer = FeedbackCreateSerializer(instance)
        
        headers = self.get_success_headers(response_serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)