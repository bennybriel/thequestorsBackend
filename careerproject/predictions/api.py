from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import CareerMatch
from .serializers import MatchSerializer
from .tasks import predict_careers_task
from django.core.cache import cache

class PredictionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Trigger async prediction task
        predict_careers_task.delay(request.user.id)
        return Response(
            {'status': 'Prediction started'},
            status=status.HTTP_202_ACCEPTED
        )

class MatchListView(generics.ListAPIView):
    serializer_class = MatchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CareerMatch.objects.filter(user=self.request.user).order_by('-match_score')

class MatchFeedbackView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            match = CareerMatch.objects.get(pk=pk, user=request.user)
            match.user_feedback = request.data.get('rating')
            match.feedback_notes = request.data.get('notes', '')
            match.save()

            # Clear cache to ensure fresh recommendations next time
            cache_key = f"user_{request.user.id}_matches"
            cache.delete(cache_key)

            return Response(
                {'status': 'Feedback saved'},
                status=status.HTTP_200_OK
            )
        except CareerMatch.DoesNotExist:
            return Response(
                {'error': 'Match not found'},
                status=status.HTTP_404_NOT_FOUND
            )