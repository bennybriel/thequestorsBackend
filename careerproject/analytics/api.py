from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import UserBehavior
from django.utils import timezone
from datetime import timedelta

class UserAnalyticsView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Track this view
        UserBehavior.objects.create(
            user=request.user,
            action='view_analytics',
            target_id=0,
            target_type='analytics'
        )

        # Get user's recent activity
        recent_actions = UserBehavior.objects.filter(
            user=request.user,
            timestamp__gte=timezone.now() - timedelta(days=30)
        ).order_by('-timestamp')[:10]

        # Get popular careers among similar users (simplified)
        popular_careers = CareerMatch.objects.filter(
            match_score__gt=70,
            user__profile__hobby_categories__overlap=request.user.profile.hobby_categories
        ).values('career__title').annotate(count=models.Count('career')).order_by('-count')[:5]

        return Response({
            'recent_actions': [
                {'action': a.action, 'target': a.target_type, 'timestamp': a.timestamp}
                for a in recent_actions
            ],
            'popular_careers': list(popular_careers)
        })