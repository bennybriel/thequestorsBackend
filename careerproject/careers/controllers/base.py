from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class BaseAPIView(APIView):
    serializer_class = None
    
    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)
    
    def success_response(self, data, status_code=status.HTTP_200_OK):
        return Response({'success': True, 'data': data}, status=status_code)
    
    def error_response(self, message, status_code=status.HTTP_400_BAD_REQUEST):
        return Response({'success': False, 'error': message}, status=status_code)
    

class BaseListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = None
    model = None
    
    def get_queryset(self):
        return self.model.objects.all()
    
    def perform_create(self, serializer):
        serializer.save()
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            'success': True,
            'data': response.data
        })

class BaseDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = None
    model = None
    
    def get_queryset(self):
        return self.model.objects.all()
    
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response({
            'success': True,
            'data': response.data
        })
    
    def handle_exception(self, exc):
        return Response({
            'success': False,
            'error': str(exc)
        }, status=status.HTTP_400_BAD_REQUEST)