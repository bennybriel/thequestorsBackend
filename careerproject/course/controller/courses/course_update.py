from decimal import Decimal
from rest_framework import generics, status
from rest_framework.response import Response
import logging
from ...serializers.courses.serial_course_update import CourseTuitionUpdateSerializer
from ...models import Course
logger = logging.getLogger(__name__)

class CourseTuitionUpdateView(generics.UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseTuitionUpdateSerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        try:
            print(request.data)
            # Convert input to Decimal if it comes as float
            if 'tuition' in request.data and isinstance(request.data['tuition'], float):
                request.data['tuition'] = Decimal(str(request.data['tuition']))
            
            if 'tuition_indigene' in request.data and isinstance(request.data['tuition_indigene'], float):
                request.data['tuition_indigene'] = Decimal(str(request.data['tuition_indigene']))

            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            
            # Save and return response
            self.perform_update(serializer)
            new_tuition = Decimal(str(serializer.validated_data['tuition']))
            new_tuition_indigene = Decimal(str(serializer.validated_data['tuition_indigene']))
            
            return Response({
                'status': 'success',
                'message': 'Tuition updated successfully',
                'tuition': f"{new_tuition:.2f}",
                'previous_tuition': f"{instance.tuition:.2f}",
                'course_id': instance.id,
                'tuition_indigene':f"{new_tuition_indigene:.2f}"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Tuition update error: {str(e)}", exc_info=True)
            return Response({
                'status': 'error',
                'message': 'Failed to update tuition',
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)