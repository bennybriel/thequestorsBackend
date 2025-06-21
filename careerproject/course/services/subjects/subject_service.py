# services/subject_service.py
from ...models import Subject

class SubjectService:
    @staticmethod
    def get_all_subjects():
        return Subject.objects.all()

    @staticmethod
    def get_active_subjects():
        return Subject.objects.filter(status=Subject.ACTIVE)

    @staticmethod
    def get_subject_by_id(subject_id):
        return Subject.objects.get(id=subject_id)

    @staticmethod
    def create_subject(validated_data):
        return Subject.objects.create(**validated_data)

    @staticmethod
    def update_subject(subject_instance, validated_data):
        for attr, value in validated_data.items():
            setattr(subject_instance, attr, value)
        subject_instance.save()
        return subject_instance

    @staticmethod
    def delete_subject(subject_instance):
        subject_instance.delete()