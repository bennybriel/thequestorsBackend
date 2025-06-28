from rest_framework import serializers

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """
    def __init__(self, *args, **kwargs):
        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', None)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        if exclude is not None:
            # Remove fields specified in the `exclude` argument
            excluded = set(exclude)
            for field_name in excluded:
                if field_name in self.fields:
                    self.fields.pop(field_name)