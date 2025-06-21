# serializers.py
from rest_framework import serializers
from .models import School, Course, Subject, UTMERequirement, OLevelRequirement
# serializers.py
from rest_framework import serializers
from io import StringIO
import csv
from .services.schools.school_service import SchoolService

from django.core.exceptions import ValidationError

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'status']
    
class CourseSerializer(serializers.ModelSerializer):
    school = SchoolSerializer(read_only=True)
    school_id = serializers.IntegerField(write_only=True)  # Changed from PrimaryKeyRelatedField

    class Meta:
        model = Course
        fields = ['id', 'name', 'school', 'school_id', 'status', 'created_at']
        read_only_fields = ['id', 'created_at', 'status']  # Added status to read_only

    def validate_school_id(self, value):
        try:
            school = School.objects.get(pk=value)
            if school.status != School.ACTIVE:
                raise serializers.ValidationError("Cannot add course to inactive school")
            return value
        except School.DoesNotExist:
            raise serializers.ValidationError("School does not exist")
    
    def validate(self, data):
        school_id = data.get('school_id')
        name = data.get('name')
        
        if school_id and name:
            if Course.objects.filter(
                name__iexact=name,
                school_id=school_id,
                status=Course.ACTIVE
            ).exists():
                raise serializers.ValidationError(
                    {"non_field_errors": ["This course already exists in the specified school"]}
                )
        
        return data
class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'guid', 'name', 'status', 'created_at']
        
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


class CourseRequirementsSerializer(serializers.Serializer):
    school = SchoolSerializer()
    course = CourseSerializer()
    utme_requirements = UTMERequirementSerializer(many=True)
    olevel_requirements = OLevelRequirementSerializer(many=True)

class SubjectUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'status']
        extra_kwargs = {
            'name': {'required': True},
            'status': {'required': True}
        }

class BulkSubjectUploadSerializer(serializers.ListSerializer):
    child = SubjectUploadSerializer()



class SubjectCSVUploadSerializer(serializers.Serializer):
    csv_file = serializers.FileField()

    def validate_csv_file(self, value):
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("Only CSV files are allowed")
        return value

    def create(self, validated_data):
        csv_file = validated_data['csv_file']
        decoded_file = csv_file.read().decode('utf-8')
        io_string = StringIO(decoded_file)
        reader = csv.DictReader(io_string)

        created_subjects = []
        for row in reader:
            subject, created = Subject.objects.get_or_create(
                name=row['name'],
                defaults={'status': row.get('status', 'active')}
            )
            if created:
                created_subjects.append(subject)

        return created_subjects



class CourseCSVUploadSerializer(serializers.Serializer):
    csv_file = serializers.FileField()

    def validate_csv_file(self, value):
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("Only CSV files are allowed")
        return value

    def try_decode(self, file_bytes):
        encodings = ['utf-8-sig', 'utf-8', 'latin-1']
        for encoding in encodings:
            try:
                return file_bytes.decode(encoding)
            except UnicodeDecodeError:
                continue
        raise serializers.ValidationError("Could not decode file. Please use UTF-8 format.")

    def create(self, validated_data):
        csv_file = validated_data['csv_file']
        file_bytes = csv_file.read()

        try:
            decoded_file = self.try_decode(file_bytes)
        except serializers.ValidationError as e:
            raise e

        io_string = StringIO(decoded_file)

        try:
            reader = csv.DictReader(io_string)
            if not reader.fieldnames:
                raise serializers.ValidationError("Empty CSV file")
        except csv.Error:
            io_string.seek(0)
            try:
                dialect = csv.Sniffer().sniff(io_string.read(1024))
                io_string.seek(0)
                reader = csv.DictReader(io_string, dialect=dialect)
            except:
                raise serializers.ValidationError("Invalid CSV format")

        required_fields = ['name', 'school_id']
        for field in required_fields:
            if field not in reader.fieldnames:
                raise serializers.ValidationError(
                    f"CSV file must contain a '{field}' column"
                )

        created_courses = []
        error_rows = []

        for i, row in enumerate(reader, start=2):
            try:
                if not row.get('name') or not row.get('school_id'):
                    raise ValueError("Name and school_id cannot be empty")

                try:
                    school = School.objects.get(id=row['school_id'])
                except School.DoesNotExist:
                    raise ValueError(f"School with ID {row['school_id']} not found")

                course, created = Course.objects.get_or_create(
                    name=row['name'].strip(),
                    school=school,
                    defaults={
                        'status': row.get('status', 'active').strip().lower() or 'active'
                    }
                )
                if created:
                    created_courses.append(course)
            except Exception as e:
                error_rows.append({
                    'row': i,
                    'error': str(e),
                    'data': row
                })

        if error_rows:
            raise serializers.ValidationError({
                'detail': f"Processed {len(created_courses)} courses successfully",
                'errors': error_rows,
                'success_count': len(created_courses)
            })

        return created_courses


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

class OLevelRequirementCSVUploadSerializer(serializers.Serializer):
    csv_file = serializers.FileField()

    # def validate_csv_file(self, value):
    #     if not value.name.endswith('.csv'):
    #         raise serializers.ValidationError("Only CSV files are allowed")
    #     return value

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

class SchoolCourseListSerializer(BaseModelSerializer):
    school_info = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'guid', 'name', 'status', 'created_at', 'school_info']

    def get_school_info(self, obj):
        return {
            'name': obj.school.name,
            'guid': obj.school.guid,
            'website': obj.school.website
        }
