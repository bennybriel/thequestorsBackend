# serializers.py
from rest_framework import serializers
from ...models import  Subject
from rest_framework import serializers
from io import StringIO
import csv

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'status']

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

