from django.urls import path
from .views import UserProfileDetailView, ProfileUpdateView

urlpatterns = [
    path('profile/', UserProfileDetailView.as_view(), name='profile-detail'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile-update'),
]