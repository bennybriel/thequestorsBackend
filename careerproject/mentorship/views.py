from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import MentorshipConnection, MentorshipMessage
from .serializers import (
    MentorshipConnectionSerializer,
    MentorshipMessageSerializer,
    MentorshipRequestSerializer
)

User = get_user_model()

class MentorshipConnectionViewSet(viewsets.ModelViewSet):
    serializer_class = MentorshipConnectionSerializer

    def get_queryset(self):
        user = self.request.user
        return MentorshipConnection.objects.filter(
            Q(mentor=user) | Q(mentee=user)
        ).select_related('mentor', 'mentee', 'career')

    def create(self, request, *args, **kwargs):
        serializer = MentorshipRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mentor = User.objects.get(id=serializer.validated_data['mentor_id'])
        if not mentor.is_mentor:
            return Response(
                {'error': 'Selected user is not a mentor'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check for existing pending/active connection
        existing = MentorshipConnection.objects.filter(
            mentor=mentor,
            mentee=request.user,
            status__in=['PENDING', 'ACTIVE']
        ).exists()

        if existing:
            return Response(
                {'error': 'A pending or active connection already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )

        connection = MentorshipConnection.objects.create(
            mentor=mentor,
            mentee=request.user,
            career_id=serializer.validated_data.get('career_id'),
            goals=serializer.validated_data.get('goals', '')
        )

        return Response(
            MentorshipConnectionSerializer(connection).data,
            status=status.HTTP_201_CREATED
        )

class MentorshipMessageViewSet(viewsets.ModelViewSet):
    serializer_class = MentorshipMessageSerializer

    def get_queryset(self):
        connection_id = self.kwargs.get('connection_id')
        return MentorshipMessage.objects.filter(
            connection_id=connection_id,
            connection__in=MentorshipConnection.objects.filter(
                Q(mentor=self.request.user) | Q(mentee=self.request.user)
            )
        ).select_related('sender').order_by('timestamp')

    def create(self, request, *args, **kwargs):
        serializer = MentorshipRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mentor = User.objects.get(id=serializer.validated_data['mentor_id'])

        # Check if user is a mentor
        if not mentor.is_mentor:
            return Response(
                {'error': 'Selected user is not a mentor'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check for existing pending/active connection
        existing = MentorshipConnection.objects.filter(
            mentor=mentor,
            mentee=request.user,
            status__in=['PENDING', 'ACTIVE']
        ).exists()

        if existing:
            return Response(
                {'error': 'A pending or active connection already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )

        connection = MentorshipConnection.objects.create(
            mentor=mentor,
            mentee=request.user,
            career_id=serializer.validated_data.get('career_id'),
            goals=serializer.validated_data.get('goals', '')
        )

        return Response(
            MentorshipConnectionSerializer(connection).data,
            status=status.HTTP_201_CREATED
        )