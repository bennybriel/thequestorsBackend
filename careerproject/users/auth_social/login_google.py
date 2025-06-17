# views.py
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
import jwt
from rest_framework.views import APIView
import datetime
from rest_framework_simplejwt.tokens import RefreshToken

class GoogleAuth(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        credential = request.data.get('credential')
        received_client_id = request.data.get('client_id')
        
        if not credential:
            return Response({'error': 'Credential is required'}, status=400)
        
        if received_client_id and received_client_id != settings.GOOGLE_OAUTH2_CLIENT_ID:
            return Response({'error': 'Invalid client ID'}, status=400)
        
        try:
            # Verify Google token
            idinfo = id_token.verify_oauth2_token(
                credential,
                requests.Request(),
                settings.GOOGLE_OAUTH2_CLIENT_ID
            )

            # Check if email is verified
            if not idinfo.get('email_verified', False):
                return Response({'error': 'Email not verified by Google'}, status=401)

            # Get or create user
            user, created = User.objects.get_or_create(
                email=idinfo['email'],
                defaults={
                    'username': idinfo['email'],
                    'first_name': idinfo.get('given_name', ''),
                    'last_name': idinfo.get('family_name', ''),
                    'is_active': True
                }
            )

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'last_name':user.last_name,
                'first_name':user.first_name,
                'is_active': user.is_active
            },
            'expireDate':datetime.datetime.now(),
            'expiresIn': 3600,
            'token': access_token,
            'idToken':str(refresh.access_token),
            'kind':"identitytoolkit#VerifyPasswordResponse",
            'localId':str(refresh.access_token),
            'refreshToken':"AMf-vBxknlI7BEle_brkV4ITkKTKrMJkgARhBpzr7_fxw4EAb04jEiNraQNAl7K81Q_ERfZt7vXSemaz6EATF8V7O",
            'registered': True,                        
            'refresh': refresh_token,
            'access': access_token,
            'message': 'Logged in successfully'
           }, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({'error': f'Invalid token: {str(e)}'}, status=400)
        except Exception as e:
            return Response({'error': f'Authentication failed: {str(e)}'}, status=500)

