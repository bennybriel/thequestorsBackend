from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import AIModelVersion, ModelTrainingLog
from .serializers import AIModelVersionSerializer, ModelTrainingLogSerializer

class AIModelVersionViewSet(viewsets.ModelViewSet):
    queryset = AIModelVersion.objects.all().order_by('-created_at')
    serializer_class = AIModelVersionSerializer

    def perform_create(self, serializer):
        if serializer.validated_data.get('is_active', False):
            AIModelVersion.objects.filter(
                model_type=serializer.validated_data['model_type']
            ).update(is_active=False)
        serializer.save()

    @action(detail=False, methods=['patch'])
    def deactivate(self, request):
        model_type = request.data.get('model_type')
        if not model_type:
            return Response(
                {'error': 'model_type is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        AIModelVersion.objects.filter(
            model_type=model_type
        ).update(is_active=False)

        return Response({'status': f'All {model_type} models deactivated'})

class ModelTrainingLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ModelTrainingLogSerializer

    def get_queryset(self):
        return ModelTrainingLog.objects.filter(
            model_version_id=self.kwargs.get('model_version_id')
        ).order_by('-training_start')