from ..models import OLevelRequirement
from ..exceptions import OLevelRequirementServiceException

class OLevelRequirementService:
    @staticmethod
    def create_olevel_requirement(school, course, subject, required_status, status):
        try:
            return OLevelRequirement.objects.create(
                school=school,
                course=course,
                subject=subject,
                required_status=required_status,
                status=status
            )
        except Exception as e:
            raise OLevelRequirementServiceException(str(e))

    @staticmethod
    def update_olevel_requirement(instance, **kwargs):
        try:
            # Only update fields that were provided
            for key, value in kwargs.items():
                setattr(instance, key, value)
            instance.save()
            return instance
        except Exception as e:
            raise OLevelRequirementServiceException(str(e))

    @staticmethod
    def delete_olevel_requirement(instance):
        try:
            instance.delete()
        except Exception as e:
            raise OLevelRequirementServiceException(str(e))