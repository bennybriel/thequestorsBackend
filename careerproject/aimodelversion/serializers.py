from rest_framework import serializers
from .models import AIModelVersion, ModelTrainingLog

class ModelTrainingLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelTrainingLog
        fields = '__all__'

class AIModelVersionSerializer(serializers.ModelSerializer):
    training_logs = ModelTrainingLogSerializer(many=True, read_only=True)

    class Meta:
        model = AIModelVersion
        fields = '__all__'