from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models import Feedback
from ..serializers.serializers import FeedbackSerializer, FeedbackCreateSerializer
from ..permissions import IsFeedbackOwnerOrReadOnly, IsAdminOrPublicReadOnly
from ..factories import FeedbackFactory
from ..exceptions import FeedbackServiceException, FeedbackNotFoundException

class FeedbackViewSet(viewsets.ModelViewSet):
    """
    Viewset for handling feedback CRUD operations
    """
    queryset = Feedback.objects.none()  # Default empty queryset
    permission_classes = [IsFeedbackOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'create':
            return FeedbackCreateSerializer
        return FeedbackSerializer

    def get_queryset(self):
        selector = FeedbackFactory.create_selector()
        
        if self.request.user.is_staff:
            return Feedback.objects.all()
        
        if self.action == 'list':
            if self.request.query_params.get('mine') == 'true':
                return selector.get_user_feedbacks(self.request.user)
            return selector.get_public_feedbacks()
        
        return super().get_queryset()

    def perform_create(self, serializer):
        service = FeedbackFactory.create_service()
        service.create_feedback(self.request.user, serializer.validated_data)

    def perform_update(self, serializer):
        service = FeedbackFactory.create_service()
        service.update_feedback(self.instance, serializer.validated_data)

    def perform_destroy(self, instance):
        service = FeedbackFactory.create_service()
        service.delete_feedback(instance)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminOrPublicReadOnly])
    def stats(self, request):
        selector = FeedbackFactory.create_selector()
        average_rating = selector.get_average_rating()
        public_count = selector.get_public_feedbacks().count()
        
        return Response({
            'average_rating': round(average_rating, 2),
            'public_feedbacks_count': public_count
        })

    def handle_exception(self, exc):
        if isinstance(exc, FeedbackNotFoundException):
            return Response(
                {'detail': str(exc)},
                status=status.HTTP_404_NOT_FOUND
            )
        elif isinstance(exc, FeedbackServiceException):
            return Response(
                {'detail': str(exc)},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().handle_exception(exc)