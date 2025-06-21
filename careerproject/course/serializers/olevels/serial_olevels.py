# serializers.py
from rest_framework import serializers
from ...models import School, Course, Subject, OLevelRequirement
from rest_framework import serializers
from io import StringIO
import csv

from django.core.exceptions import ValidationError
class OLevelRequirementSerializer(serializers.ModelSerializer):
    school_id = serializers.PrimaryKeyRelatedField(
        queryset=School.objects.all(), 
        source='school',
        required=False  # Make optional for updates
    )
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), 
        source='course',
        required=False  # Make optional for updates
    )
    subject_id = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(), 
        source='subject',
        required=False  # Make optional for updates
    )
    
    class Meta:
        model = OLevelRequirement
        fields = [
            'id',
            'school_id',
            'course_id',
            'subject_id',
            'required_status',
            'status',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'required_status': {'required': False}  # Also make optional for updates
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make fields required for creation
        if self.instance is None:
            self.fields['school_id'].required = True
            self.fields['course_id'].required = True
            self.fields['subject_id'].required = True
            self.fields['required_status'].required = True

    def validate(self, data):
        instance = getattr(self, 'instance', None)
        
        # Get current or new values
        school = data.get('school', instance.school if instance else None)
        course = data.get('course', instance.course if instance else None)
        subject = data.get('subject', instance.subject if instance else None)

        # Check if we're changing the unique-together fields
        if instance:  # Update operation
            if (school and school != instance.school) or \
               (course and course != instance.course) or \
               (subject and subject != instance.subject):
                if OLevelRequirement.objects.filter(
                    school=school or instance.school,
                    course=course or instance.course,
                    subject=subject or instance.subject
                ).exclude(pk=instance.pk).exists():
                    raise serializers.ValidationError(
                        "This combination of school, course and subject already exists."
                    )
        else:  # Create operation
            if OLevelRequirement.objects.filter(
                school=school,
                course=course,
                subject=subject
            ).exists():
                raise serializers.ValidationError(
                    "This combination of school, course and subject already exists."
                )
        return data
        
    def update(self, instance, validated_data):
        # Only update fields that are provided in the request
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    def validate_required_status(self, value):
        if value not in dict(OLevelRequirement.REQUIRED_STATUS_CHOICES):
            raise serializers.ValidationError(
                f"Invalid required_status. Must be one of: {', '.join([choice[0] for choice in OLevelRequirement.REQUIRED_STATUS_CHOICES])}"
            )
        return value

class OLevelRequirementCSVUploadSerializer(serializers.Serializer):
    csv_file = serializers.FileField()

    def create(self, validated_data):
        csv_file = validated_data['csv_file']
        decoded_file = csv_file.read().decode('utf-8-sig')  # Handle BOM
        io_string = StringIO(decoded_file)

        reader = csv.DictReader(io_string)
        required_columns = ['school_id', 'course_id', 'subject_id', 'required_status']

        # Validate columns
        missing_columns = [col for col in required_columns if col not in reader.fieldnames]
        if missing_columns:
            raise serializers.ValidationError(
                f"Missing required columns: {', '.join(missing_columns)}"
            )

        created_requirements = []
        error_rows = []

        for row_num, row in enumerate(reader, start=2):  # Row numbers start at 2 (header is 1)
            try:
                # Validate required fields
                if not all(row.get(col) for col in required_columns):
                    raise ValueError("All required columns must have values")

                # Get related objects
                try:
                    school = School.objects.get(id=row['school_id'])
                    course = Course.objects.get(id=row['course_id'], school=school)
                    subject = Subject.objects.get(id=row['subject_id'])
                except School.DoesNotExist:
                    raise ValueError(f"School with ID {row['school_id']} not found")
                except Course.DoesNotExist:
                    raise ValueError(f"Course with ID {row['course_id']} not found in this school")
                except Subject.DoesNotExist:
                    raise ValueError(f"Subject with ID {row['subject_id']} not found")

                # Validate required_status
                valid_statuses = ['required', 'recommended', 'not_required']
                if row['required_status'].lower() not in valid_statuses:
                    raise ValueError(f"Invalid required_status. Must be one of: {', '.join(valid_statuses)}")

                # Create or update requirement
                requirement, created = OLevelRequirement.objects.update_or_create(
                    school=school,
                    course=course,
                    subject=subject,
                    defaults={
                        'required_status': row['required_status'].lower(),
                        'status': row.get('status', 'active').lower() or 'active'
                    }
                )

                created_requirements.append(requirement)

            except Exception as e:
                error_rows.append({
                    'row': row_num,
                    'error': str(e),
                    'data': row
                })

        if error_rows:
            raise serializers.ValidationError({
                'detail': f"Processed {len(created_requirements)} requirements successfully",
                'errors': error_rows,
                'success_count': len(created_requirements)
            })

        return created_requirements