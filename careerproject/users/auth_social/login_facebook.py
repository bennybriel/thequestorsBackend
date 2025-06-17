# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
import datetime
import requests as http_requests
import json

class FacebookAuth(APIView):
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