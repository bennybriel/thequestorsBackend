# services/school_service.py
from typing import Optional, Dict, Any
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError
from django.db import models, IntegrityError
from ..base_service import BaseService
from ...models import School
import uuid
class SchoolService(BaseService[School]):
    model_class = School

    def get_all(self, **filters) -> models.QuerySet:
        """Get all schools with optional filters"""
        return self.model_class.objects.filter(**filters).order_by('name')

    def get_by_id(self, id: int) -> Optional[School]:
        """Get school by ID or return None"""
        try:
            return self.model_class.objects.get(id=id)
        except ObjectDoesNotExist:
            return None

    def get_by_name(self, name: str) -> Optional[School]:
        """Case-insensitive search by school name"""
        try:
            return self.model_class.objects.get(name__iexact=name)
        except ObjectDoesNotExist:
            return None
        except self.model_class.MultipleObjectsReturned:
            return self.model_class.objects.filter(name__iexact=name).first()

    def validate_uniqueness(self, name: str, exclude_id: int = None) -> None:
        """Public method for name uniqueness validation"""
        self.validate_school_data({'name': name}, exclude_id=exclude_id)

    def get_by_website(self, website: str) -> Optional[School]:
        """Case-insensitive search by school website"""
        try:
            return self.model_class.objects.get(website__iexact=website)
        except ObjectDoesNotExist:
            return None
        except self.model_class.MultipleObjectsReturned:
            return self.model_class.objects.filter(website__iexact=website).first()

    # services/school_service.py
    def validate_school_data(self, data: Dict[str, Any], exclude_id: int = None) -> None:
        """Validate school data including uniqueness checks"""
        # Name validation - only check if name is in the update data
        if 'name' in data:
            existing = self.get_by_name(data['name'])
            if existing and (exclude_id is None or existing.id != exclude_id):
                raise ValidationError(
                    {'name': 'A school with this name already exists'},
                    code='duplicate_name'
                )

        # Website validation - only check if website is in the update data
        if 'website' in data:
            existing = self.get_by_website(data['website'])
            if existing and (exclude_id is None or existing.id != exclude_id):
                raise ValidationError(
                    {'website': 'A school with this website already exists'},
                    code='duplicate_website'
                )

        # Status validation
        if 'status' in data and data['status'] not in dict(School.STATUS_CHOICES):
            raise ValidationError(
                {'status': 'Invalid status value'},
                code='invalid_status'
            )


    def create(self, data: Dict[str, Any]) -> School:
        """Create new school with validation"""
        uid = str(uuid.uuid4())  # Convert UUID to string for storage
        data['uid'] = uid  # Add the UUID to the data dictionary
        
        # Validate both the UUID and the provided data
        self.validate_school_data({'uid': uid})  # Validate the UUID
        self.validate_school_data(data)  # Validate the complete data
        
        try:
            return self.model_class.objects.create(**data)
        except IntegrityError as e:
            raise ValidationError(
                {'database': str(e)},
                code='integrity_error'
            )
            
    def update(self, id: int, data: Dict[str, Any], partial: bool = False) -> School:
        school = self.get_by_id(id)
        if not school:
            raise ObjectDoesNotExist(f"School with id {id} does not exist")

        # Prepare data for validation
        if partial:
            # For PATCH, only validate provided fields
            validation_data = {k: v for k, v in data.items() if k in ['name', 'website', 'status']}
        else:
            # For PUT, use provided values or existing values
            validation_data = {
                'name': data.get('name', school.name),
                'website': data.get('website', school.website),
                'status': data.get('status', school.status)
            }

        # Skip name validation if name isn't being changed
        if 'name' in validation_data and validation_data['name'] == school.name:
            validation_data.pop('name', None)
        
        # Skip website validation if website isn't being changed
        if 'website' in validation_data and validation_data['website'] == school.website:
            validation_data.pop('website', None)

        # Only validate if there are fields to validate
        if validation_data:
            self.validate_school_data(validation_data, exclude_id=id)

        # Apply updates
        for field, value in data.items():
            setattr(school, field, value)
        
        school.save()
        return school

    def delete(self, id: int) -> bool:
        """Delete school by ID"""
        school = self.get_by_id(id)
        if school:
            try:
                school.delete()
                return True
            except Exception as e:
                raise ValidationError(
                    {'database': f'Delete failed: {str(e)}'},
                    code='delete_error'
                )
        return False

    def activate(self, id: int) -> School:
        """Set school status to active"""
        return self.update_status(id, School.ACTIVE)

    def deactivate(self, id: int) -> School:
        """Set school status to inactive"""
        return self.update_status(id, School.INACTIVE)

    def update_status(self, id: int, status: str) -> School:
        """Update school status with validation"""
        if status not in dict(School.STATUS_CHOICES):
            raise ValidationError(
                {'status': 'Invalid status value'},
                code='invalid_status'
            )
        return self.update(id, {'status': status})