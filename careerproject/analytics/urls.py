from django.urls import path
from .views import (
    TrackUserBehaviorView,
    CareerTrendListView,
    UserActivityView
)

urlpatterns = [
    path('track/', TrackUserBehaviorView.as_view(), name='track-behavior'),
    path('trends/', CareerTrendListView.as_view(), name='career-trends'),
    path('activity/', UserActivityView.as_view(), name='user-activity'),
]