from decimal import Decimal
from rest_framework import serializers
from ...models import Course

class CourseTuitionUpdateSerializer(serializers.ModelSerializer):
    tuition = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True,
        help_text="New tuition value (positive decimal number)"
    )
    tuition_indigene = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True,
        help_text="New tuition indigene value (positive decimal number)"
    )

    class Meta:
        model = Course
        fields = ['tuition','tuition_indigene']

    def validate_tuition(self, value):
        """Comprehensive decimal validation"""
        if not isinstance(value, Decimal):
            try:
                value = Decimal(str(value))
            except:
                raise serializers.ValidationError("Invalid decimal value")

        if value < Decimal('0'):
            raise serializers.ValidationError("Tuition must be positive")

        if value > Decimal('1000000000'):
            raise serializers.ValidationError("Maximum tuition is 100,000")

        # Get current tuition as Decimal
        instance = self.instance
        if instance and hasattr(instance, 'tuition') and instance.tuition:
            current_tuition = Decimal(str(instance.tuition))
            max_reduction = current_tuition * Decimal('0.8')
            
            # if value < max_reduction:
            #     raise serializers.ValidationError(
            #         f"Cannot reduce tuition by more than 20%. Minimum allowed: {max_reduction:.2f}"
            #     )

        return value