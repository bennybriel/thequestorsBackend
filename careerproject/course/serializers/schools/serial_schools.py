# serializers.py
from rest_framework import serializers
from ...models import School, Course, Subject
from rest_framework import serializers
from io import StringIO
import csv
from ...services.schools.school_service import SchoolService
from ..base import BaseModelSerializer

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'
        read_only_fields = ('created_at',)

    # serializers.py
    def validate(self, attrs):
        try:
            service = SchoolService()
            if self.instance:  # Update case
                # For updates, only validate fields that are being changed
                validation_data = {}
                for field in ['name', 'website', 'status']:
                    if field in attrs and getattr(self.instance, field) != attrs[field]:
                        validation_data[field] = attrs[field]
                
                if validation_data:
                    service.validate_school_data(validation_data, exclude_id=self.instance.id)
            else:  # Create case
                service.validate_school_data(attrs)
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        
        return attrs

    def validate_status(self, value):
        if value not in dict(School.STATUS_CHOICES).keys():
            raise serializers.ValidationError("Invalid status value")
        return value   
class SchoolUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'status']
        extra_kwargs = {
            'name': {'required': True},
            'status': {'required': True}
        }


class SchoolCSVUploadSerializer(serializers.Serializer):
    csv_file = serializers.FileField()

    def validate_csv_file(self, value):
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("Only CSV files are allowed")
        return value

    def try_decode(self, file_bytes):
        # Try common encodings in order
        encodings = ['utf-8-sig', 'utf-8', 'latin-1', 'iso-8859-1', 'windows-1252']

        for encoding in encodings:
            try:
                return file_bytes.decode(encoding)
            except UnicodeDecodeError:
                continue
        raise serializers.ValidationError(
            "Could not decode file. Please save as UTF-8 format."
        )

    def create(self, validated_data):
        csv_file = validated_data['csv_file']
        file_bytes = csv_file.read()

        try:
            decoded_file = self.try_decode(file_bytes)
        except serializers.ValidationError as e:
            raise e

        io_string = StringIO(decoded_file)

        # Try to read CSV with different dialects
        try:
            reader = csv.DictReader(io_string)
            if not reader.fieldnames:
                raise serializers.ValidationError("Empty CSV file")
        except csv.Error:
            # Try with different delimiters if standard reading fails
            io_string.seek(0)
            try:
                dialect = csv.Sniffer().sniff(io_string.read(1024))
                io_string.seek(0)
                reader = csv.DictReader(io_string, dialect=dialect)
            except:
                raise serializers.ValidationError("Invalid CSV format")

        if 'name' not in reader.fieldnames:
            raise serializers.ValidationError(
                "CSV file must contain a 'name' column"
            )

        created_subjects = []
        error_rows = []

        for i, row in enumerate(reader, start=2):  # start=2 to account for header row
            try:
                if not row.get('name'):
                    raise ValueError("Name cannot be empty")

                subject, created = School.objects.get_or_create(
                    name=row['name'].strip(),
                    defaults={
                        'status': row.get('status', 'active').strip().lower() or 'active'
                    }
                )
                if created:
                    created_subjects.append(subject)
            except Exception as e:
                error_rows.append({
                    'row': i,
                    'error': str(e),
                    'data': row
                })

        if error_rows:
            raise serializers.ValidationError({
                'detail': f"Processed {len(created_subjects)} subjects successfully",
                'errors': error_rows,
                'success_count': len(created_subjects)
            })

        return created_subjects
    
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
