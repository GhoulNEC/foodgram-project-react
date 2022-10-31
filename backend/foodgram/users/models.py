from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import UsernameValidator


class CustomUser(AbstractUser):
    username_validator = UsernameValidator
    username = models.CharField(
        'Логин пользователя',
        max_length=settings.MAX_SIGNUP_PARAMS_LENGTH,
        unique=True,
        validators=[username_validator],
    )
    first_name = models.CharField(
        'Имя пользователя',
        max_length=settings.MAX_SIGNUP_PARAMS_LENGTH,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия пользователя',
        max_length=settings.MAX_SIGNUP_PARAMS_LENGTH,
        blank=True
    )
    email = models.EmailField(
        'Email',
        max_length=settings.MAX_EMAIL_LENGTH,
        unique=True
    )
    password = models.CharField(
        'Пароль',
        max_length=settings.MAX_SIGNUP_PARAMS_LENGTH
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=settings.MAX_CONFIRMCODE_LENGTH,
        null=True
    )

    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username
