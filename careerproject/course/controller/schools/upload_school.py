# views.py (add this to your existing views)
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from ...serializers.schools.serial_schools import SchoolCSVUploadSerializer,SchoolUploadSerializer,SchoolSerializer
# views.py
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status


class SchoolUploadView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, JSONParser]

    def post(self, request, format=None):
        # Handle single subject upload
        if isinstance(request.data, dict):
            serializer = SchoolUploadSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Handle bulk subject upload
        # elif isinstance(request.data, list):
        #     serializer = BulkSubjectUploadSerializer(data=request.data, many=True)
        #     if serializer.is_valid():
        #         serializer.save()
        #         return Response(serializer.data, status=status.HTTP_201_CREATED)
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"error": "Invalid data format"},
            status=status.HTTP_400_BAD_REQUEST
        )

class SchoolCSVUploadView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        # if not request.user.has_perm('your_app.add_subject'):
        #     return Response(
        #         {"detail": "You do not have permission to perform this action."},
        #         status=status.HTTP_403_FORBIDDEN
        #     )

        serializer = SchoolCSVUploadSerializer(data=request.data)
        if serializer.is_valid():
            try:
                created_subjects = serializer.save()
                return Response(
                    {
                        "detail": f"Successfully uploaded {len(created_subjects)} subjects",
                        "count": len(created_subjects),
                        "subjects": SchoolSerializer(created_subjects, many=True).data
                    },
                    status=status.HTTP_201_CREATED
                )
            except serializers.ValidationError as e:
                return Response(
                    e.detail,
                    status=status.HTTP_400_BAD_REQUEST
                )
            except Exception as e:
                return Response(
                    {"detail": f"Server error: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
