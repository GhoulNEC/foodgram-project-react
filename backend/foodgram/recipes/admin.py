from django.contrib import admin

from .models import (Amount, Cart, Favorite, Follow, Ingredient, Recipe, Tag,
                     TagRecipe)


class AmountAdmin(admin.ModelAdmin):
    list_display = ('pk', 'ingredient', 'amount', 'recipe')
    search_fields = ('ingredient',)
    empty_value_display = '-пусто-'


class CartsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    search_fields = ('user__username', 'author__username')


class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    search_fields = ('user__username', 'recipe__name')
    empty_value_display = '-пусто-'


class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')
    search_fields = ('user__username', 'author__username')


class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class RecipesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'name', 'text', 'cooking_time', 'image',
                    'pub_date')
    search_fields = ('author__username', 'name')
    empty_value_display = '-пусто-'


class TagsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', 'color')
    search_fields = ('name', 'slug')
    empty_list_display = '-пусто-'


class TagsRecipesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'tag', 'recipe')
    search_fields = ('tag__name', 'recipe__name')
    empty_list_display = '-пусто-'


admin.site.register(Amount, AmountAdmin)
admin.site.register(Cart, CartsAdmin)
admin.site.register(Favorite, FavoritesAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Ingredient, IngredientsAdmin)
admin.site.register(Recipe, RecipesAdmin)
admin.site.register(Tag, TagsAdmin)
admin.site.register(TagRecipe, TagsRecipesAdmin)
