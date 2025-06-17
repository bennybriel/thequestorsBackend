from rest_framework import serializers
from .models import CareerMatch, PredictionSession
from careers.serializers import CareerSerializer
from users.serializers import UserSerializer


class CareerMatchSerializer(serializers.ModelSerializer):
    career = CareerSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = CareerMatch
        fields = '__all__'

class PredictionSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredictionSession
        fields = '__all__'