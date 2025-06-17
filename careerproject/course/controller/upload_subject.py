# views.py (add this to your existing views)
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..serializers import SubjectUploadSerializer,SubjectSerializer, SubjectCSVUploadSerializer
# views.py
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status


class SubjectUploadView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, JSONParser]

    def post(self, request, format=None):
        # Handle single subject upload
        if isinstance(request.data, dict):
            serializer = SubjectUploadSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Handle bulk subject upload
        elif isinstance(request.data, list):
            serializer = BulkSubjectUploadSerializer(data=request.data, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"error": "Invalid data format"},
            status=status.HTTP_400_BAD_REQUEST
        )

class SubjectCSVUploadView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        serializer = SubjectCSVUploadSerializer(data=request.data)
        if serializer.is_valid():
            try:
                created_subjects = serializer.save()
                return Response(
                    {
                        "detail": f"Successfully uploaded {len(created_subjects)} subjects",
                        "subjects": SubjectSerializer(created_subjects, many=True).data
                    },
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response(
                    {"detail": f"Error processing CSV: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)