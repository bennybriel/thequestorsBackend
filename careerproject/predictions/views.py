from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import CareerMatch, PredictionSession
from .serializers import CareerMatchSerializer, PredictionSessionSerializer

class CareerMatchViewSet(viewsets.ModelViewSet):
    serializer_class = CareerMatchSerializer

    def get_queryset(self):
        return CareerMatch.objects.filter(user=self.request.user)

class PredictionSessionViewSet(viewsets.ModelViewSet):
    serializer_class = PredictionSessionSerializer

    def get_queryset(self):
        return PredictionSession.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def predict(self, request):
        # This would call your AI model to generate predictions
        # Implementation depends on your AI setup
        return Response({'status': 'Prediction started'})