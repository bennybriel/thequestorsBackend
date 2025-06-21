# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ...serializers.subjects.serial_subjets import SubjectSerializer
from ...services.subjects.subject_service import SubjectService
from ...models import Subject

class SubjectAPIView(APIView):
    """
    Base class for Subject views to inherit common functionality
    """
    service_class = SubjectService
    serializer_class = SubjectSerializer

    def get_service(self):
        return self.service_class()

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)

class SubjectListCreateView(SubjectAPIView):
    """
    List all subjects or create a new subject
    """
    def get(self, request, *args, **kwargs):
        service = self.get_service()
        subjects = service.get_all_subjects()
        serializer = self.get_serializer(subjects, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            service = self.get_service()
            subject = service.create_subject(serializer.validated_data)
            response_serializer = self.get_serializer(subject)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubjectRetrieveUpdateDestroyView(SubjectAPIView):
    """
    Retrieve, update or delete a subject instance
    """
    def get_object(self, pk):
        service = self.get_service()
        try:
            return service.get_subject_by_id(pk)
        except Subject.DoesNotExist:
            return None

    def get(self, request, pk, *args, **kwargs):
        subject = self.get_object(pk)
        if not subject:
            return Response(
                {"detail": "Subject not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(subject)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        subject = self.get_object(pk)
        if not subject:
            return Response(
                {"detail": "Subject not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(subject, data=request.data, partial=False)
        if serializer.is_valid():
            service = self.get_service()
            updated_subject = service.update_subject(subject, serializer.validated_data)
            response_serializer = self.get_serializer(updated_subject)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, *args, **kwargs):
        subject = self.get_object(pk)
        if not subject:
            return Response(
                {"detail": "Subject not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(subject, data=request.data, partial=True)
        if serializer.is_valid():
            service = self.get_service()
            updated_subject = service.update_subject(subject, serializer.validated_data)
            response_serializer = self.get_serializer(updated_subject)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        subject = self.get_object(pk)
        if not subject:
            return Response(
                {"detail": "Subject not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        service = self.get_service()
        service.delete_subject(subject)
        return Response(status=status.HTTP_204_NO_CONTENT)