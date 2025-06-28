from rest_framework import serializers
from ..models.career import CareerPath, ProfessionalQualification
from rest_framework import serializers
from ..models.career import CareerPath, ProfessionalQualification
from .base import DynamicFieldsModelSerializer

class ProfessionalQualificationSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = ProfessionalQualification
        fields = '__all__'

class CareerPathSerializer(DynamicFieldsModelSerializer):
    qualifications = ProfessionalQualificationSerializer(many=True, read_only=True)
    
    class Meta:
        model = CareerPath
        fields = '__all__'
        


class ProfessionalQualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalQualification
        fields = '__all__'
        extra_kwargs = {
            'career_path': {'read_only': True}
        }

class CareerPathSerializer(serializers.ModelSerializer):
    qualifications = ProfessionalQualificationSerializer(many=True, read_only=True)
    
    class Meta:
        model = CareerPath
        fields = '__all__'