from django.core.validators import MinValueValidator
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
    slug = models.SlugField(
        'Слаг тега',
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
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=10,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} {self.measurement_unit}'


class Follow(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('author',)

    def __str__(self):
        return self.author


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='recipes'
    )
    name = models.CharField(
        'Название рецепта',
        max_length=50,
        help_text='Укажите название рецепта'
    )
    text = models.CharField(
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
        upload_to='recipes/images/',
        help_text='Добавьте картинку блюда'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name[:15]


class TagRecipe(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Тег',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Тег рецепта'
        verbose_name_plural = 'Теги рецептов'
        ordering = ('recipe__name', 'tag__name',)

    def __str__(self):
        return f'{self.recipe}: {self.tag}'


class Favorite(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='selected_user'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='selected_recipe'
    )

    class Meta:
        verbose_name = 'Рецепт в избранном'
        verbose_name_plural = 'Рецепты в избранном'
        ordering = ('recipe',)

    def __str__(self):
        return f'{self.user}: {self.recipe}'


class Cart(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='cart'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='cart'
    )

    class Meta:
        verbose_name = 'Корзина пользователя'
        verbose_name_plural = 'Корзины пользователей'
        ordering = ('user__username', 'recipe__name')

    def __str__(self):
        return self.recipe


class Amount(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=(
            MinValueValidator(
                1,
                'Блюдо не может существовать без ингредиентов!'
            ),
        ),
    )

    class Meta:
        verbose_name = 'Количество'
        ordering = ('recipe__name', 'ingredient__name')

    def __str__(self):
        return (f'{self.recipe.name}: {self.amount} '
                f'{self.ingredient.measurement_unit}')
