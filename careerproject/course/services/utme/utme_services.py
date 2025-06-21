# from ..models import UTMERequirement
from ...models import UTMERequirement
from ...exceptions import UTMERequirementServiceException

class UTMERequirementService:
    @staticmethod
    def create_utme_requirement(school, course, subject, required_status, status):
        if course.school != school:
            raise UTMERequirementServiceException("Course doesn't belong to the specified school")
        
        if course.status != Course.ACTIVE:
            raise UTMERequirementServiceException("Course is not active")
            
        if subject.status != Subject.ACTIVE:
            raise UTMERequirementServiceException("Subject is not active")
            
        if UTMERequirement.objects.filter(
            school=school,
            course=course,
            subject=subject
        ).exists():
            raise UTMERequirementServiceException("Requirement combination already exists")
            
        return UTMERequirement.objects.create(
            school=school,
            course=course,
            subject=subject,
            required_status=required_status,
            status=status
        )

    @staticmethod
    def update_utme_requirement(instance, **validated_data):
        # Prevent changing school, course, or subject
        for field in ['school', 'course', 'subject']:
            if field in validated_data:
                if getattr(instance, field) != validated_data[field]:
                    raise UTMERequirementServiceException(f"Cannot change {field} after creation")
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        instance.save()
        return instance

    @staticmethod
    def delete_utme_requirement(instance):
        instance.delete()
        
# class UTMERequirementService:
#     @staticmethod
#     def get_requirements_by_school(school_id):
#         return UTMERequirement.objects.filter(school_id=school_id, status=UTMERequirement.ACTIVE)
    
#     @staticmethod
#     def get_requirements_by_course(course_id):
#         return UTMERequirement.objects.filter(course_id=course_id, status=UTMERequirement.ACTIVE)
    
#     @staticmethod
#     def create_requirement(data):
#         return UTMERequirement.objects.create(**data)
    
#     @staticmethod
#     def update_requirement(instance, validated_data):
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()
#         return instance