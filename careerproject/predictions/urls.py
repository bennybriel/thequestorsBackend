from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CareerMatchViewSet, PredictionSessionViewSet

router = DefaultRouter()
router.register(r'matches', CareerMatchViewSet, basename='match')
router.register(r'sessions', PredictionSessionViewSet, basename='session')

urlpatterns = [
    path('', include(router.urls)),
    path('predict/', PredictionSessionViewSet.as_view({'post': 'predict'}), name='predict'),
]