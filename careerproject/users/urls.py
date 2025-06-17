from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, CustomTokenObtainPairView, LoginView,UserDetailView,VerifyTokenView,UserProfileView, GoogleAuth
#from .auth_social.login_google import GoogleAuth
from .auth_social.login_facebook import FacebookAuth

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth-register'),
    path('login/', LoginView.as_view(), name='auth-login'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserDetailView.as_view(), name='user-profile'),
    path('verify/', VerifyTokenView.as_view(), name='verify-token'),
    path('profile/', UserProfileView.as_view(), name='verify-token'),
    path('google_login/', GoogleAuth.as_view(), name='google-auth'),      
    path('facebook_login/', FacebookAuth.as_view(), name='facebook-auth'),      
]