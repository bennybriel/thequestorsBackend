from rest_framework import serializers
from ..models.education import EducationPath, University, UniversityCareerPath

class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = '__all__'

class UniversityCareerPathSerializer(serializers.ModelSerializer):
    university = UniversitySerializer(read_only=True)
    
    class Meta:
        model = UniversityCareerPath
        fields = '__all__'
        extra_kwargs = {
            'career_path': {'read_only': True}
        }

class EducationPathSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationPath
        fields = '__all__'
        extra_kwargs = {
            'career_path': {'read_only': True}
        }