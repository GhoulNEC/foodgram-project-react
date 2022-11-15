from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from .validators import UsernameValidator


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=settings.MAX_SIGNUP_PARAMS_LENGTH,
        unique=True,
        db_index=True,
        verbose_name='Логин',
        help_text='Введите логин',
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z'
            ),
            UsernameValidator(),
        ]
    )
    email = models.EmailField(
        max_length=settings.MAX_EMAIL_LENGTH,
        unique=True,
        blank=False,
        db_index=True,
        verbose_name='Электронная почта',
        help_text='Введите электронную почту'
    )
    first_name = models.CharField(
        max_length=settings.MAX_SIGNUP_PARAMS_LENGTH,
        blank=False,
        verbose_name='Имя пользователя',
        help_text='Введите имя пользователя'
    )
    last_name = models.CharField(
        max_length=settings.MAX_SIGNUP_PARAMS_LENGTH,
        blank=False,
        verbose_name='Фамилия пользователя',
        help_text='Введите фамилию пользователя'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ('-date_joined',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'Автор: {self.author} - Подписчик: {self.user}'
