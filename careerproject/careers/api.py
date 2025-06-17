from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from .models import Career, LearningResource
from .serializers import CareerSerializer, ResourceSerializer

class CareerListView(generics.ListAPIView):
    queryset = Career.objects.all()
    serializer_class = CareerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'required_skills']

class CareerDetailView(generics.RetrieveAPIView):
    queryset = Career.objects.all()
    serializer_class = CareerSerializer
    permission_classes = [IsAuthenticated]

class CareerResourcesView(generics.ListAPIView):
    serializer_class = ResourceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        career_id = self.kwargs['pk']
        return LearningResource.objects.filter(career_id=career_id)