from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserBehavior, CareerTrend
from .serializers import UserBehaviorSerializer, CareerTrendSerializer

class TrackUserBehaviorView(generics.CreateAPIView):
    serializer_class = UserBehaviorSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CareerTrendListView(generics.ListAPIView):
    serializer_class = CareerTrendSerializer
    queryset = CareerTrend.objects.all().order_by('-date')

    def get_queryset(self):
        queryset = super().get_queryset()
        career_id = self.request.query_params.get('career_id')
        if career_id:
            queryset = queryset.filter(career_id=career_id)
        return queryset[:30]  # Limit to 30 most recent entries

class UserActivityView(generics.ListAPIView):
    serializer_class = UserBehaviorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserBehavior.objects.filter(
            user=self.request.user
        ).order_by('-timestamp')[:50]  # Last 50 actions