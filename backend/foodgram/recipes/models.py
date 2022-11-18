from colorfield.fields import ColorField
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from users.models import CustomUser


class Tag(models.Model):
    name = models.CharField(
        max_length=settings.MAX_MODEL_FIELD_NAME_LENGTH,
        unique=True,
        verbose_name='Тег',
        help_text='Введите название Тега'
    )
    color = ColorField(
        max_length=settings.MAX_MODEL_FIELD_COLOR_LENGTH,
        format='hexa',
        unique=True,
        verbose_name='HEX-код цвета',
        help_text='Введите цветовой HEX-код'
    )
    slug = models.SlugField(
        max_length=settings.MAX_MODEL_FIELD_NAME_LENGTH,
        unique=True,
        verbose_name='Slug тега',
        help_text='Введите slug тега'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name[:30]


class Ingredient(models.Model):
    name = models.CharField(
        max_length=settings.MAX_MODEL_FIELD_NAME_LENGTH,
        verbose_name='Название ингредиента',
        help_text='Введите название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=settings.MAX_MODEL_FIELD_NAME_LENGTH,
        verbose_name='Единица измерения',
        help_text='Введите единицу измерения'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name} {self.measurement_unit}'


class Recipe(models.Model):
    author = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(
        max_length=settings.MAX_MODEL_FIELD_NAME_LENGTH,
        db_index=True,
        verbose_name='Название рецепта',
        help_text='Введите название рецепта'
    )
    image = models.ImageField(
        upload_to='recipes/images',
        blank=True,
        null=True,
        verbose_name='Изображение блюда',
        help_text='Добавьте изображение Вашего блюда'
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
        help_text='Введите описание рецепта'
    )
    ingredients = models.ManyToManyField(
        to=Ingredient,
        through='RecipeIngredient',
        related_name='recipes',
        verbose_name='Ингредиенты рецепта',
        help_text='Добавьте ингредиенты'
    )
    tags = models.ManyToManyField(
        to=Tag,
        related_name='recipes'
    )
    cooking_time = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(
                limit_value=settings.MIN_COOKING_TIME,
                message=settings.VALIDATOR_MESSAGE.format(
                    min_value=settings.MIN_COOKING_TIME
                )
            )
        ],
        verbose_name='Время приготовления'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации рецепта'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name[:30]


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        to=Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredient'
    )
    ingredient = models.ForeignKey(
        to=Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredient'
    )
    amount = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(
                limit_value=settings.MIN_INGREDIENT_AMOUNT,
                message=settings.VALIDATOR_MESSAGE.format(
                    min_value=settings.MIN_INGREDIENT_AMOUNT
                )
            )
        ],
        verbose_name='Количество ингредиентов'
    )

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'

    def __str__(self):
        return (
            f'{self.ingredient.name}: {self.amount} '
            f'{self.ingredient.measurement_unit}'
        )


class Favorite(models.Model):
    user = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    recipe = models.ForeignKey(
        to=Recipe,
        on_delete=models.CASCADE,
        related_name='is_favorited'
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return (
            f'Пользователь: {self.user.username} - '
            f'Рецепт в избранном: {self.recipe.name}'
        )


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name='cart_user'
    )
    recipe = models.ForeignKey(
        to=Recipe,
        on_delete=models.CASCADE,
        related_name='cart_recipe'
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return (
            f'Пользователь: {self.user.username} - '
            f'Рецепт: {self.recipe.name}'
        )
