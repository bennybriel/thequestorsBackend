# serializers.py
from rest_framework import serializers
from ...models import School, Course
from rest_framework import serializers
from io import StringIO
import csv
from ...services.schools.school_service import SchoolService
from django.core.exceptions import ValidationError
from rest_framework import serializers
from ...serializers.schools.serial_schools import SchoolSerializer
from ...serializers.olevels.serial_olevels import  OLevelRequirementSerializer
from ...serializers.utme.serial_utme import UTMERequirementSerializer
 
    
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
        


class CourseRequirementsSerializer(serializers.Serializer):
    school = SchoolSerializer()
    course = CourseSerializer()
    utme_requirements = UTMERequirementSerializer(many=True)
    olevel_requirements = OLevelRequirementSerializer(many=True)


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
