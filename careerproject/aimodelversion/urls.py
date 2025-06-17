from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AIModelVersionViewSet, ModelTrainingLogViewSet

router = DefaultRouter()
router.register(r'models', AIModelVersionViewSet, basename='model')
router.register(r'models/(?P<model_version_id>\d+)/training-logs', ModelTrainingLogViewSet, basename='training-log')

urlpatterns = [
    path('', include(router.urls)),
]