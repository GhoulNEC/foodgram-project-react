from rest_framework import serializers


class UniqueFieldsValidator:
    """
    Validator checks unique fields in serializer.
    """
    message = 'Подписка на самого себя - невозможна!'

    def __init__(self, field_1, field_2, message=None):
        self.field_1 = field_1
        self.field_2 = field_2
        self.message = message or self.message

    def __call__(self, data):
        if data[self.field_1] == data[self.field_2]:
            raise serializers.ValidationError(self.message)
