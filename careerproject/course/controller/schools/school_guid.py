import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ...models import School
from ...serializers.schools.serial_schools import SchoolSerializer

class SchoolGuidUpdateView(APIView):
    def get(self, request):
        schools = School.objects.all()
        serializer = SchoolSerializer(schools, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            schools = School.objects.all()
            updated_schools = []
            
            for school in schools:
                school.guid = uuid.uuid4()
                school.save()
                updated_schools.append(school)
            
            serializer = SchoolSerializer(updated_schools, many=True)
            return Response({
                'message': 'Successfully updated GUIDs for all schools',
                'schools': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)