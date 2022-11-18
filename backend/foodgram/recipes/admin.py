from django.contrib import admin
from django.utils.html import format_html

from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)

admin.site.empty_value_display = '-пусто-'


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    search_fields = ('user', 'recipe')
    list_filter = ('user', 'recipe')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'name', 'get_ingredients', 'cooking_time',
                    'get_favorite_list_size', 'get_tags')
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('name', 'author', 'tags')
    fields = ('author', 'name', 'text', 'image', 'cooking_time', 'tags',
              'get_favorite_list_size')
    readonly_fields = ('get_favorite_list_size',)
    inlines = (RecipeIngredientInline,)

    def get_favorite_list_size(self, obj):
        return Favorite.objects.filter(recipe=obj).count()

    def get_tags(self, obj):
        return list(obj.tags.all())

    def get_ingredients(self, obj):
        return list(RecipeIngredient.objects.filter(recipe=obj))

    get_favorite_list_size.short_description = 'Добавления рецепта в избранное'
    get_tags.short_description = 'Теги'
    get_ingredients.short_description = 'Ингредиенты'


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'amount', 'ingredient')
    list_display_links = ('ingredient',)
    search_fields = ('ingredient__name',)
    list_filter = ('ingredient',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    search_fields = ('user', 'recipe')
    list_filter = ('user', 'recipe')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'get_color', 'slug')
    list_display_links = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)

    def get_color(self, obj):
        return format_html(
            f'<spawn style="color: {obj.color};">{obj.color}</spawn>'
        )

    get_color.short_description = 'Цвет'
