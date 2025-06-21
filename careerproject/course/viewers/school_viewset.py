# views/school_viewset.py
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from ..serializers.schools.serial_schools import SchoolSerializer
from ..services.schools.school_service import SchoolService
from .base_viewset import BaseViewSet

class SchoolViewSet(BaseViewSet):
    service_class = SchoolService
    serializer_class = SchoolSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        status = self.request.query_params.get('status', None)
        filters = {}
        if status:
            filters['status'] = status
        return self.service_class().get_all(**filters)