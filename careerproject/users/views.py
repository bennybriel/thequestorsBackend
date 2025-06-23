from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate
from .serializers import UserSerializer, CustomTokenObtainPairSerializer, LoginSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework.authtoken.models import Token
User = get_user_model()
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
import logging
from google.auth.transport import requests as google_requests
import json
from django.http import JsonResponse
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
import datetime
from .services.email_service import EmailService
import os
from django.conf import settings
import uuid

logger = logging.getLogger(__name__)
User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
           
            verification_url = settings.QUESTORS_URL
            if user : 
                success, response = EmailService.send_signup_email(user, verification_url)
                
            # Generate tokens for immediate login after registration
            refresh = RefreshToken.for_user(user)
            
            response_data = {
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'expireDate': datetime.datetime.now().isoformat(),
                'expiresIn': 3600,
                'token': str(refresh.access_token),
                'idToken': str(refresh.access_token),
                'kind': "identitytoolkit#VerifyPasswordResponse",
                'localId': user.id,  # Changed to actual user ID
                'refreshToken': str(refresh),  # Changed to actual refresh token
                'registered': True,
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Handle specific exceptions if needed
            error_data = {
                'error': {
                    'statuscode':'ERRORS',
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Registration failed ',
                    'errors': [str(e)] if str(e) else ['An unexpected error occurred']
                }
            }
            print(error_data);
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'last_name':user.last_name, 
                'first_name':user.first_name,
                'is_active': user.is_active,
                'is_staff': user.is_staff,
                'date_joined':user.date_joined
                
            },
            'expireDate':datetime.datetime.now(),
            'expiresIn': 3600,
            'token': str(refresh.access_token),
            'idToken':str(refresh.access_token),
            'kind':"identitytoolkit#VerifyPasswordResponse",
            'localId':str(refresh.access_token),
            'refreshToken':"AMf-vBxknlI7BEle_brkV4ITkKTKrMJkgARhBpzr7_fxw4EAb04jEiNraQNAl7K81Q_ERfZt7vXSemaz6EATF8V7O",
            'registered': True,                        
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'Logged in successfully'
        }, status=status.HTTP_200_OK)
    

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


# class GoogleLogin(APIView):
#     authentication_classes = []
#     permission_classes = []

#     def post(self, request):
#         try:
#             # Get token from request body
#             body = json.loads(request.body.decode('utf-8'))
#             token = body.get('token')
#             uid = uuid.uuid4()
#             if not token:
#                 return JsonResponse(
#                     {'error': 'Token is required'},
#                     status=400
#                 )

#             # Verify token
#             idinfo = id_token.verify_oauth2_token(
#                 token,
#                 google_requests.Request(),
#                 settings.GOOGLE_OAUTH2_CLIENT_ID
#             )

#             # Validate token
#             if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
#                 raise ValueError('Invalid issuer')

#             if idinfo['aud'] != settings.GOOGLE_OAUTH2_CLIENT_ID:
#                 raise ValueError('Invalid audience')

#             # Get or create user
#             user, created = User.objects.get_or_create(
#                 email=idinfo['email'],
#                 defaults={
#                     'username': idinfo['email'].split('@')[0],
#                     'first_name': idinfo.get('given_name', ''),
#                     'last_name': idinfo.get('family_name', ''),
#                     'guid':uuid
#                 }
#             )

#             # Generate JWT tokens
#             refresh = RefreshToken.for_user(user)

#             return Response({
#                 'user': {
#                     'id': user.id,
#                     'username': user.username,
#                     'email': user.email,
#                     'last_name':user.last_name,
#                     'first_name':user.first_name,
#                     'is_active': user.is_active,
#                     'is_staff': user.is_staff
#                 },
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#                 'message': 'Logged in successfully'
#             }, status=status.HTTP_200_OK)

#         except ValueError as e:
#             return JsonResponse(
#                 {'error': str(e)},
#                 status=401
#             )
#         except Exception as e:
#             return JsonResponse(
#                 {'error': 'Authentication failed'},
#                 status=500
#             )

class VerifyTokenView(APIView):
    """
    Verify the authenticity of an access token
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # If the request reaches this point, the token is valid
        # (thanks to IsAuthenticated permission)
        return Response(
            {
                "message": "Token is valid",
                "user": {
                    "id": request.user.id,
                    "username": request.user.username,
                    "email": request.user.email
                }
            },
            status=status.HTTP_200_OK
        )


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        data = request.data

        # Update allowed fields
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)
        user.username = data.get('username', user.username)

        try:
            user.save()
            return Response({
                'message': 'Profile updated successfully',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
            
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
        uid = uuid.uuid4()
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
                    'is_active': True,
                    'guid': uid
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
                'is_active': user.is_active,
                'is_staff':user.is_staff
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


class SocialAuth(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        provider = request.data.get('provider')  # 'google' or 'facebook'
        credential = request.data.get('credential')
        access_token = request.data.get('access_token')  # For Facebook
        
        if not provider or (not credential and not access_token):
            return Response({'error': 'Provider and credentials are required'}, status=400)

        try:
            if provider == 'google':
                return self.handle_google_auth(credential)
            elif provider == 'facebook':
                return self.handle_facebook_auth(access_token)
            else:
                return Response({'error': 'Invalid provider'}, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

    def handle_google_auth(self, credential):
        # Existing Google auth logic
        idinfo = id_token.verify_oauth2_token(
            credential,
            requests.Request(),
            settings.GOOGLE_OAUTH2_CLIENT_ID
        )
        email = idinfo['email']
        first_name = idinfo.get('given_name', '')
        last_name = idinfo.get('family_name', '')
        return self.create_or_get_user(email, first_name, last_name)

    def handle_facebook_auth(self, access_token):
        # Verify Facebook token
        app_id = settings.FACEBOOK_APP_ID
        app_secret = settings.FACEBOOK_APP_SECRET
        debug_token_url = f"https://graph.facebook.com/debug_token?input_token={access_token}&access_token={app_id}|{app_secret}"
        
        response = http_requests.get(debug_token_url)
        data = response.json()
        
        if 'error' in data or not data.get('data', {}).get('is_valid', False):
            raise ValueError('Invalid Facebook token')
        
        user_id = data['data']['user_id']
        fields = 'id,email,first_name,last_name'
        user_info_url = f"https://graph.facebook.com/{user_id}?fields={fields}&access_token={access_token}"
        
        user_response = http_requests.get(user_info_url)
        user_data = user_response.json()
        
        if 'error' in user_data:
            raise ValueError('Failed to fetch user info from Facebook')
        
        email = user_data.get('email')
        if not email:
            raise ValueError('Email not provided by Facebook')
            
        return self.create_or_get_user(
            email,
            user_data.get('first_name', ''),
            user_data.get('last_name', '')
        )

    def create_or_get_user(self, email, first_name, last_name):
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': email,
                'first_name': first_name,
                'last_name': last_name,
                'is_active': True
            }
        )
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'email': user.email,
                'firstName': user.first_name,
                'lastName': user.last_name
            }
        })

def send_verification_email(user):
    verification_url = f"https://example.com/verify/{user.id}/"
    success, response = EmailService.send_signup_email(user, verification_url)
    
    if not success:
        print(f"Failed to send email: {response}")
        # Handle error