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
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.parsers import JSONParser
from ..services.parsing.nlp_parser import NLPParser
from ..services.matching.similarity_matcher import SimilarityMatcher
from ..models.user import UserProfile
import logging
from django.conf import settings
logger = logging.getLogger(__name__)

class CareerSearchView(GenericViewSet):
    parser_classes = [JSONParser]  # Now properly imported
    
    @action(detail=False, methods=['POST'], url_path='search')
    def career_search(self, request):
        """
        Validate and process career search request
        Example payload:
        {
            "search_input": "I love coding in Python and want to work at a tech company"
        }
        """
        try:
            # Input validation
            if not request.data or 'search_input' not in request.data:
                raise ValidationError("'search_input' field is required")
            
            search_input = request.data['search_input'].strip()
            
            if len(search_input) < 10:
                raise ValidationError("Search input must be at least 10 characters")
                
            if len(search_input) > 1000:
                raise ValidationError("Search input cannot exceed 1000 characters")
            
            # Get user profile
            user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
            
            # Parse input
            parser = NLPParser()
            parsed_data = parser.parse(search_input)
            
            # Update profile (save search history)
            user_profile.search_history.append({
                'input': search_input,
                'timestamp': str(timezone.now()),
                'parsed_data': parsed_data
            })
            user_profile.save()
            
            # Match careers
            matcher = SimilarityMatcher()
            matches = matcher.match(parsed_data)
            
            # Format response
            return Response({
                'success': True,
                'matches': matches,
                'meta': {
                    'input_length': len(search_input),
                    'match_count': len(matches),
                    'top_match_score': max(m['match_score'] for m in matches) if matches else 0
                }
            }, status=status.HTTP_200_OK)
            
        except ValidationError as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Career search failed: {str(e)}", exc_info=True)
            
            error_message = "Internal server error"
            error_detail = str(e) if settings.DEBUG else None
            
            return Response(
                {
                    'success': False,
                    'error': error_message,
                    'detail': error_detail  # Only shown in debug mode
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# class CareerSearchView(BaseAPIView):
#     def post(self, request):
#         try:
#             user = request.user
#             user_profile = UserProfile.objects.get(user=user)
            
#             # Parse input
#             parser = NLPParser()
#             parsed_data = parser.parse(request.data.get('search_input', ''))
            
#             # Update user profile
#             user_profile.hobbies = parsed_data.get('hobbies', [])
#             user_profile.passions = parsed_data.get('passions', [])
#             user_profile.vision = parsed_data.get('vision', '')
#             user_profile.dream = parsed_data.get('dream', '')
#             user_profile.save()
            
#             # Match careers
#             matcher = SimilarityMatcher()
#             matches = matcher.match(parsed_data)
            
#             return self.success_response({'matches': matches})
        
#         except Exception as e:
#             return self.error_response(str(e))

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