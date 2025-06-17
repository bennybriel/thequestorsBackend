from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models import OLevelRequirement
from ..serializers import OLevelRequirementSerializer
from ..permissions import IsAdminOrReadOnly, IsSchoolAdminOrReadOnly
from ..services.olevel_service import OLevelRequirementService
from ..selectors import OLevelRequirementSelector
from ..exceptions import OLevelRequirementServiceException

class OLevelRequirementViewSet(viewsets.ModelViewSet):
    queryset = OLevelRequirement.objects.all()
    serializer_class = OLevelRequirementSerializer
    #permission_classes = [IsAdminOrReadOnly | IsSchoolAdminOrReadOnly]

    def get_queryset(self):
        filters = {}
        
        if 'school_id' in self.request.query_params:
            filters['school_id'] = self.request.query_params['school_id']
        if 'course_id' in self.request.query_params:
            filters['course_id'] = self.request.query_params['course_id']
        if 'subject_id' in self.request.query_params:
            filters['subject_id'] = self.request.query_params['subject_id']
        if 'required_status' in self.request.query_params:
            filters['required_status'] = self.request.query_params['required_status']
        if 'status' in self.request.query_params:
            filters['status'] = self.request.query_params['status']
        if 'search' in self.request.query_params:
            filters['search'] = self.request.query_params['search']
            
        return OLevelRequirementSelector.list_olevel_requirements(filters)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            instance = OLevelRequirementService.create_olevel_requirement(
                school=serializer.validated_data['school'],
                course=serializer.validated_data['course'],
                subject=serializer.validated_data['subject'],
                required_status=serializer.validated_data['required_status'],
                status=serializer.validated_data['status']
            )
        except OLevelRequirementServiceException as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        headers = self.get_success_headers(serializer.data)
        return Response(
            self.get_serializer(instance).data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True  # This is key for partial updates
        )
        serializer.is_valid(raise_exception=True)
        
        try:
            self.perform_update(serializer)
        except OLevelRequirementServiceException as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        return Response(serializer.data)

    def perform_update(self, serializer):
        # Additional business logic if needed
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        try:
            OLevelRequirementService.delete_olevel_requirement(instance)
        except OLevelRequirementServiceException as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def status_choices(self, request):
        return Response({
            'required_status_choices': OLevelRequirement.REQUIRED_STATUS_CHOICES,
            'status_choices': OLevelRequirement.STATUS_CHOICES
        })