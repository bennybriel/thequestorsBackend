from rest_framework.exceptions import ValidationError

def validate_required_status(value):
    valid_statuses = [choice[0] for choice in OLevelRequirement.REQUIRED_STATUS_CHOICES]
    if value not in valid_statuses:
        raise ValidationError(f"Invalid required status. Must be one of: {', '.join(valid_statuses)}")

def validate_status(value):
    valid_statuses = [choice[0] for choice in OLevelRequirement.STATUS_CHOICES]
    if value not in valid_statuses:
        raise ValidationError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")