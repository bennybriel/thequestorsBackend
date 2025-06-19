from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import get_user_model
from ..serializers import UserSerializer, UserPermissionSerializer
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from ..permissions import IsStaffUser
from rest_framework import status
from rest_framework.permissions import IsAdminUser


User = get_user_model()

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class RegisteredUsersListView(APIView):
    #permission_classes = [permissions.IsAdminUser]  # Only admins can access
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active', 'date_joined']
    filter_backends = [SearchFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    permission_classes = [IsStaffUser]  # Custom permission class
    
    def get(self, request):
        try:
            queryset = User.objects.all().order_by('-date_joined')
            
            # Apply pagination
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(queryset, request)
            
            if page is not None:
                serializer = UserSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)
            
            serializer = UserSerializer(queryset, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserPermissionView(APIView):
    """
    Endpoint to check and update user staff/admin permissions
    Requires admin privileges to access
    """
    permission_classes = [IsAdminUser]
    
    def get(self, request, email):
        try:
            user = User.objects.get(email=email)
            serializer = UserPermissionSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def patch(self, request, email):
        try:
            user = User.objects.get(email=email)
            serializer = UserPermissionSerializer(user, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
            
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )