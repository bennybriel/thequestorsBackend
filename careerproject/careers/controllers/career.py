from rest_framework import status
from ..services.parsing.nlp_parser import NLPParser
from ..services.matching.similarity_matcher import SimilarityMatcher
from ..services.generation.plan_generator import PlanGenerator
from ..services.generation.pdf_generator import PdfGenerator
from .base import BaseAPIView
from ..models.user import UserProfile
from rest_framework import generics
from ..models.career import CareerPath, ProfessionalQualification
from .base import BaseListView, BaseDetailView
from ..serializers.career import (CareerPathSerializer, ProfessionalQualificationSerializer)


class CareerSearchView(BaseAPIView):
    def post(self, request):
        try:
            user = request.user
            user_profile = UserProfile.objects.get(user=user)
            
            # Parse input
            parser = NLPParser()
            parsed_data = parser.parse(request.data.get('search_input', ''))
            
            # Update user profile
            user_profile.hobbies = parsed_data.get('hobbies', [])
            user_profile.passions = parsed_data.get('passions', [])
            user_profile.vision = parsed_data.get('vision', '')
            user_profile.dream = parsed_data.get('dream', '')
            user_profile.save()
            
            # Match careers
            matcher = SimilarityMatcher()
            matches = matcher.match(parsed_data)
            
            return self.success_response({'matches': matches})
        
        except Exception as e:
            return self.error_response(str(e))

class CareerPlanView(BaseAPIView):
    def get(self, request, career_id):
        try:
            user = request.user
            user_profile = UserProfile.objects.get(user=user)
            
            # Generate plan
            generator = PlanGenerator()
            plan_data = generator.generate(
                career_id,
                {
                    'hobbies': user_profile.hobbies,
                    'passions': user_profile.passions,
                    'vision': user_profile.vision,
                    'dream': user_profile.dream
                }
            )
            
            return self.success_response({'plan': plan_data})
        
        except Exception as e:
            return self.error_response(str(e))

class CareerPlanPDFView(BaseAPIView):
    def get(self, request, career_id):
        try:
            user = request.user
            user_profile = UserProfile.objects.get(user=user)
            
            # Generate plan
            generator = PlanGenerator()
            plan_data = generator.generate(
                career_id,
                {
                    'hobbies': user_profile.hobbies,
                    'passions': user_profile.passions,
                    'vision': user_profile.vision,
                    'dream': user_profile.dream
                }
            )
            
            # Generate PDF
            pdf_generator = PdfGenerator()
            pdf = pdf_generator.generate_pdf(plan_data)
            
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="career_plan_{user.username}.pdf"'
            return response
        
        except Exception as e:
            return self.error_response(str(e))



class CareerPathListView(BaseListView):
    serializer_class = CareerPathSerializer
    model = CareerPath
    permission_classes = []  # Public access
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if 'industry' in self.request.query_params:
            queryset = queryset.filter(
                industry=self.request.query_params['industry'])
        return queryset

class CareerPathDetailView(BaseDetailView):
    serializer_class = CareerPathSerializer
    model = CareerPath
    permission_classes = []  # Public access

class ProfessionalQualificationListView(BaseListView):
    serializer_class = ProfessionalQualificationSerializer
    model = ProfessionalQualification
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if 'career_path' in self.request.query_params:
            queryset = queryset.filter(
                career_path_id=self.request.query_params['career_path'])
        return queryset

class ProfessionalQualificationDetailView(BaseDetailView):
    serializer_class = ProfessionalQualificationSerializer
    model = ProfessionalQualification