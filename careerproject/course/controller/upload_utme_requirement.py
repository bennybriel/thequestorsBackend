# views.py
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from ..serializers import UTMERequirementSerializer,UTMERequirementCSVUploadSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class UTMERequirementCSVUploadView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        # if not request.user.has_perm('your_app.change_utmerequirement'):
        #     return Response(
        #         {"detail": "You do not have permission to perform this action."},
        #         status=status.HTTP_403_FORBIDDEN
        #     )

        serializer = UTMERequirementCSVUploadSerializer(data=request.data)
        if serializer.is_valid():
            try:
                requirements = serializer.save()
                return Response(
                    {
                        "detail": f"Successfully processed {len(requirements)} UTME requirements",
                        "count": len(requirements),
                        "requirements": UTMERequirementSerializer(requirements, many=True).data
                    },
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response(
                    {"detail": f"Server error: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)