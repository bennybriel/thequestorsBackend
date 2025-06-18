from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from ..services.email_service import EmailService
from ..utils.tokens import generate_password_reset_token, verify_password_reset_token
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect
from django.conf import settings
#from django.shortcuts import redirect
import urllib.parse

User = get_user_model()

class PasswordResetRequestView(APIView):
    """
    Handle password reset requests
    """
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response(
                {'error': 'Email is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
            
            # Generate reset token and URL
            token = generate_password_reset_token(user)
            reset_url = request.build_absolute_uri(
                f'/api/v1/auth/password-reset-confirm/{user.guid}/{token}/'
            )
            
            # Send password reset email
            success, response = EmailService.send_password_reset_email(user, reset_url)
            if success:
                return Response(
                    {   'status_code':201,
                        'message': 'Password reset email sent',
                        'email': user.email,
                        'reset_url': reset_url  # For testing, remove in production
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                {
                    'error': 'Failed to send password reset email',
                    'details': response
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
                
        except User.DoesNotExist:
            return Response(
                {'error': 'No user found with this email address'},
                status=status.HTTP_404_NOT_FOUND
            )



class PasswordResetConfirmView(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, user_id, token):
        """
        Handle GET request - show password reset form
        """
        print(token)
        try:
            # Verify the token is valid (but don't reset yet)
            #uid = force_str(urlsafe_base64_decode(user_id))
        
            user = User.objects.get(guid=user_id)
            
                
            if not verify_password_reset_token(user, token):
                return redirect(
                f"{settings.QUESTORS_URL}/#/login"
               )
            params = urllib.parse.urlencode({
                'guid': str(user.guid),
                'token':token
            })
            
            return redirect(
                f"{settings.QUESTORS_URL}/#/reset-password?{params}"
            )
            
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(
                {"error": "Invalid reset link"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request):
        """
        Handle POST request - actually reset the password
        """
        try:
            token =request.data.get('token')
            guid =request.data.get('guid')
            user = User.objects.get(guid=guid)
            
            if not verify_password_reset_token(user, token):
                return Response(
                    {"error": "Invalid or expired reset link"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            password = request.data.get('password')
            confirm_password = request.data.get('confirm_password')
            
            if password != confirm_password:
                return Response(
                    {"error": "Passwords do not match"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user.set_password(password)
            user.save()
            return Response({"message": "Password reset successfully"})
            
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(
                {"error": "Invalid reset link"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

      