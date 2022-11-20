from django.conf import settings
from djoser import serializers as djoser_serializers
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueTogetherValidator

from .validators import UniqueFieldsValidator
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from users.models import CustomUser, Follow


class UserSerializer(djoser_serializers.UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')
        read_only_fields = ('id',)
        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': True
            }
        }

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return request and obj.follower.filter(author=obj.id).exists()

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=['user', 'recipe'],
                message='Рецепт уже добавлен в избранное'
            )
        ]


class IngredientSerializer(serializers.ModelSerializer):
    measurement_unit = serializers.ReadOnlyField()

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = ('name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = ('name', 'color', 'slug')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField()
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    tags = TagSerializer(many=True, read_only=True)
    ingredients = RecipeIngredientSerializer(source='recipe_ingredient',
                                             many=True)
    image = Base64ImageField(max_length=None, use_url=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        return (request and request.user.is_authenticated
                and obj.is_favorited.filter(user=request.user).exists())

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        return (request and request.user.is_authenticated
                and obj.cart_recipe.filter(user=request.user).exists())

    def validate(self, data):
        tags = self.initial_data.get('tags')
        if not tags:
            raise serializers.ValidationError(
                {'tags': 'Тег должен быть добавлен'}
            )
        tag_list = []
        for tag in tags:
            tag_obj = get_object_or_404(Tag, id=tag)
            if tag_obj in tag_list:
                raise serializers.ValidationError(
                    {'tags': f'Тег {tag_obj.name} уже добавлен'}
                )
            tag_list.append(tag_obj)

        recipe_ingredient = data['recipe_ingredient']
        if not recipe_ingredient:
            raise serializers.ValidationError(
                'Рецепт не может быть без ингредиентов'
            )
        ingredients_list = []
        for item in recipe_ingredient:
            item_data = list(item.values())
            ingredient_obj = get_object_or_404(
                Ingredient, id=item_data[0]['id'])
            if ingredient_obj in ingredients_list:
                raise serializers.ValidationError(
                    {
                        "ingredients":
                            f'Ингредиент {ingredient_obj.name} уже добавлен'
                    }
                )
            ingredients_list.append(ingredient_obj)
            if item_data[1] < 1:
                raise serializers.ValidationError(
                    {
                        "amount": {
                            f'ingredient - {ingredient_obj.name}':
                                settings.VALIDATOR_MESSAGE.format(
                                    min_value=settings.MIN_INGREDIENT_AMOUNT)}
                    }
                )

        return data

    def add_ingredients_and_tags(self, instance, ingredients, tags):
        ingredients_list = [
            RecipeIngredient(
                recipe=instance,
                ingredient=get_object_or_404(
                    Ingredient, id=obj['ingredient']['id']),
                amount=obj['amount']
            ) for obj in ingredients
        ]
        RecipeIngredient.objects.bulk_create(ingredients_list)
        instance.tags.set(tags)
        return instance

    def create(self, validated_data):
        ingredients = validated_data.pop('recipe_ingredient')
        tags = self.initial_data.get('tags')
        recipe = Recipe.objects.create(
            author=self.context.get('request').user,
            image=validated_data.pop('image'),
            **validated_data
        )
        return self.add_ingredients_and_tags(recipe, ingredients, tags)

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('recipe_ingredient')
        tags = self.initial_data.get('tags')
        instance.ingredients.clear()
        instance.tags.clear()
        instance = self.add_ingredients_and_tags(instance, ingredients, tags)
        return super().update(instance, validated_data)


class ListRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class ShoppingCartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=['user', 'recipe'],
                message='Рецепт уже добавлен в корзину'
            )
        ]


class FollowSerializer(UserSerializer):
    recipes = ListRecipeSerializer(many=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('recipes', 'recipes_count')

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class FollowerSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Follow
        fields = ('user', 'author')
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'author'],
                message='Вы уже подписаны на этого автора'
            ),
            UniqueFieldsValidator('user', 'author')
        ]
