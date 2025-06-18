from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, CustomTokenObtainPairView, LoginView,UserDetailView,VerifyTokenView,UserProfileView, GoogleAuth
#from .auth_social.login_google import GoogleAuth
from .auth_social.login_facebook import FacebookAuth
from .controller.reset_password import PasswordResetConfirmView,PasswordResetRequestView
from .controller.guid import UserGuidUpdateView

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
    path('password-reset/', PasswordResetRequestView.as_view(), name='api-password-reset'),
    path('password-reset-confirm/<str:user_id>/<str:token>/', PasswordResetConfirmView.as_view(), name='api-password-reset-confirm'),   
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),   
    path('update-guids/', UserGuidUpdateView.as_view(), name='update-user-guids'),
]