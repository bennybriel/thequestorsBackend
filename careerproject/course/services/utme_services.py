from ..models import UTMERequirement

class UTMERequirementService:
    @staticmethod
    def get_requirements_by_school(school_id):
        return UTMERequirement.objects.filter(school_id=school_id, status=UTMERequirement.ACTIVE)
    
    @staticmethod
    def get_requirements_by_course(course_id):
        return UTMERequirement.objects.filter(course_id=course_id, status=UTMERequirement.ACTIVE)
    
    @staticmethod
    def create_requirement(data):
        return UTMERequirement.objects.create(**data)
    
    @staticmethod
    def update_requirement(instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance