import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import CustomUser
from ..serializers import UserSerializer

class UserGuidUpdateView(APIView):
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            users = CustomUser.objects.all()
            updated_users = []
            
            for user in users:
                user.guid = uuid.uuid4()
                user.save()
                updated_users.append(user)
            
            serializer = UserSerializer(updated_users, many=True)
            return Response({
                'message': 'Successfully updated GUIDs for all users',
                'users': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)