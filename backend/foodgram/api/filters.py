from django_filters import rest_framework
from recipes.models import Recipe, Tag
from rest_framework.filters import SearchFilter


class RecipeFilter(rest_framework.FilterSet):
    author = rest_framework.AllValuesMultipleFilter(field_name='author__id')
    tags = rest_framework.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug'
    )
    is_favorited = rest_framework.BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = rest_framework.BooleanFilter(
        method='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('author__id', 'tags__slug', 'is_favorited',
                  'is_in_shopping_cart')

    def get_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(is_favorited__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(cart_recipe__user=self.request.user)
        return queryset


class IngredientFilter(SearchFilter):
    search_param = 'name'
