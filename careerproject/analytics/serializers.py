from rest_framework import serializers
from .models import UserBehavior, CareerTrend
from careers.serializers import CareerSerializer

class UserBehaviorSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBehavior
        fields = '__all__'
        read_only_fields = ('timestamp',)

class CareerTrendSerializer(serializers.ModelSerializer):
    career = CareerSerializer(read_only=True)

    class Meta:
        model = CareerTrend
        fields = '__all__'