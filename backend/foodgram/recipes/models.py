from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import CustomUser


class Tag(models.Model):
    name = models.CharField(
        'Название тега',
        max_length=20,
        unique=True,
    )
    color = models.CharField(
        'HEX-код цвета',
        max_length=16,
        blank=True,
        null=True
    )
    slug = models.CharField(
        'Слаг тега',
        max_length=30,
        unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        'Ингредиент',
        max_length=30,
    )
    measurement_unit = models.TextField(
        'Единица измерения',
        max_length=10,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='recipes'
    )
    name = models.TextField(
        'Название рецепта',
        max_length=50,
        help_text='Укажите название рецепта'
    )
    text = models.TextField(
        'Описание рецепта',
        max_length=250,
        help_text='Укажите описание рецепта'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=(
            MinValueValidator(
                1,
                'Поправьте время приготовления, оно слишком короткое!'
            ),
        ),
        help_text='Укажите время приготовления в минутах'
    )
    image = models.ImageField(
        'Фото блюда',
        upload_to='recipes/',
        help_text='Добавьте картинку блюда'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
        related_name='recipes',
        help_text='Выберите тег для блюда'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        related_name='recipes',
        help_text='Выберите необходимые ингредиенты для приготовления блюда'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name
