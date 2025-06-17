from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..base_views import BaseListCreateView, BaseRetrieveUpdateDestroyView
from ..models import UTMERequirement
from ..serializers import UTMERequirementSerializer
from ..filters import UTMERequirementFilter

class UTMERequirementListCreateView(BaseListCreateView):
    queryset = UTMERequirement.objects.all()
    serializer_class = UTMERequirementSerializer
    filterset_class = UTMERequirementFilter
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['created_at', 'school__name', 'course__name', 'subject__name']

class UTMERequirementRetrieveUpdateDestroyView(BaseRetrieveUpdateDestroyView):
    queryset = UTMERequirement.objects.all()
    serializer_class = UTMERequirementSerializer
    
    def put(self, request, *args, **kwargs):
        # For PUT requests, we'll treat them as PATCH to allow partial updates
        return self.partial_update(request, *args, **kwargs)