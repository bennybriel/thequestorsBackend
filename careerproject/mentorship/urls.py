from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MentorshipConnectionViewSet, MentorshipMessageViewSet

router = DefaultRouter()
router.register(r'connections', MentorshipConnectionViewSet, basename='connection')
router.register(r'connections/(?P<connection_id>\d+)/messages', MentorshipMessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]