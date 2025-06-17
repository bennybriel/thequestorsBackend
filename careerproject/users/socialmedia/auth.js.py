from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class GoogleLoginView(APIView):
    def post(self, request):
        token = request.data.get('token')

        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request())

            email = idinfo['email']
            name = idinfo.get('name', '')

            user, created = User.objects.get_or_create(email=email, defaults={'username': email, 'first_name': name})

            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })

        except Exception as e:
            return Response({'error': 'Invalid token', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)
