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
    # Correct read-only fields (ensure they match your model relationships)
    school_name = serializers.CharField(source='school.name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    subjects = serializers.CharField(source='subject.name', read_only=True)
    school_id = serializers.IntegerField(source='school.id', read_only=True)
    course_id = serializers.IntegerField(source='course.id', read_only=True)
    subject_id = serializers.IntegerField(source='subject.id', read_only=True)

    class Meta:
        model = UTMERequirement
        fields = [
            'id',
            # Required fields for creation
            'school', 'course', 'subject', 'required_status', 'status',
            # Read-only display fields
            'school_name', 'course_name', 'subjects',
            'school_id', 'course_id', 'subject_id',
            'created_at'
        ]
        extra_kwargs = {
            'school': {'write_only': True},
            'course': {'write_only': True},
            'subject': {'write_only': True},
            'required_status': {'required': True},
            'status': {'required': False, 'default': 'active'}

        }

    def validate(self, data):
        """Validate all required relationships exist"""
        required_relations = ['school', 'course', 'subject']
        for relation in required_relations:
            if relation not in data:
                raise serializers.ValidationError(
                    {relation: "This field is required"}
                )
            if not data[relation].pk:
                raise serializers.ValidationError(
                    {relation: "Related object does not exist"}
                )
        return data

    def create(self, validated_data):
        """Handle creation with proper error messages"""
        try:
            return super().create(validated_data)
        except IntegrityError as e:
            if 'null value' in str(e):
                field = str(e).split('"')[1]
                raise serializers.ValidationError(
                    {field: "This field cannot be null"}
                )
            raise serializers.ValidationError(
                {"database_error": str(e)}
            )