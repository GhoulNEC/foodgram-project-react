from django.core.validators import BaseValidator
from rest_framework.serializers import ValidationError


class UsernameValidator(BaseValidator):
    forbidden_username = ['me', 'admin']
    message = 'Нельзя использовать логин {username}'

    def __init__(self, forbidden_username=None, message=None):
        self.forbidden_username = forbidden_username or self.forbidden_username
        self.message = message or self.message

    def __call__(self, data):
        username = data.lower()
        if username in self.forbidden_username:
            raise ValidationError(
                self.message.format(username=username)
            )
