from rest_framework import serializers

class BaseModelSerializer(serializers.ModelSerializer):
    guid = serializers.UUIDField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        fields = ['id', 'guid', 'created_at']