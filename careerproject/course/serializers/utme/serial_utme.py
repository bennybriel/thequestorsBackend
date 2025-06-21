# serializers.py
from rest_framework import serializers
from ...models import School, Course, Subject,UTMERequirement
from rest_framework import serializers
from io import StringIO
import csv

class UTMERequirementCSVUploadSerializer(serializers.Serializer):
    csv_file = serializers.FileField()

    def validate_csv_file(self, value):
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("Only CSV files are allowed")
        return value

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

                # Create or update requirement
                requirement, created = UTMERequirement.objects.update_or_create(
                    school=school,
                    course=course,
                    subject=subject,
                    defaults={
                        'required_status': row['required_status'].lower(),
                        'status': row.get('status', 'active').lower()
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


class UTMERequirementSerializer(serializers.ModelSerializer):
    schoolname = serializers.CharField(source='school.name', read_only=True)
    coursename = serializers.CharField(source='course.name', read_only=True)
    subjectname = serializers.CharField(source='subject.name', read_only=True)
    schoolID = serializers.IntegerField(source='school.id', read_only=True)
    courseID = serializers.IntegerField(source='course.id', read_only=True)
    subjectId = serializers.IntegerField(source='subject.id', read_only=True)
    
    # Status fields
    course_status = serializers.CharField(source='course.status', read_only=True)
    subject_status = serializers.CharField(source='subject.status', read_only=True)
    requirement_status = serializers.CharField(source='get_required_status_display', read_only=True)
    active_status = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = UTMERequirement
        fields = [
            # Identification fields
            'id', 
            
            # Name fields
            'schoolname', 'coursename', 'subjectname',
            
            # ID fields
            'schoolID', 'courseID', 'subjectId',
            
            # Status fields
            'required_status', 'requirement_status',
            'status', 'active_status',
            'course_status', 'subject_status',
            
            # Timestamp
            'created_at'
        ]
        read_only_fields = ('created_at', 'requirement_status', 'active_status', 
                          'course_status', 'subject_status')
        extra_kwargs = {
            'required_status': {'required': True},  # Make required for both create and update
            'status': {'required': False}  # Default will be applied if not provided
        }
    
    def validate(self, data):
        # Only check unique constraint during creation
        if self.instance is None:  # This is a create operation
            if 'school' in data and 'course' in data and 'subject' in data:
                if UTMERequirement.objects.filter(
                    school=data['school'],
                    course=data['course'],
                    subject=data['subject']
                ).exists():
                    raise serializers.ValidationError("This requirement combination already exists.")
            
            # Ensure required_status is provided during creation
            if 'required_status' not in data:
                raise serializers.ValidationError({
                    'required_status': 'This field is required when creating a new requirement.'
                })
        
        return data


