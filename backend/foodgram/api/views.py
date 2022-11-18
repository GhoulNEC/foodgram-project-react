from django.db.models import Sum
from djoser import views as djoser_views
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from users.models import CustomUser, Follow

from .filters import IngredientFilter, RecipeFilter
from .mixins import AddDelMixin
from .pagination import CustomPagination
from .pdf_generator import generate_pdf
from .permissions import IsAdminOrAuthor
from .serializers import (FavoriteSerializer, FollowerSerializer,
                          FollowSerializer, IngredientSerializer,
                          ListRecipeSerializer, RecipeSerializer,
                          ShoppingCartSerializer, TagSerializer,
                          UserSerializer)


class UserViewSet(djoser_views.UserViewSet, AddDelMixin):
    serializer_class = UserSerializer
    mixin_serializer = FollowSerializer
    model_class = CustomUser
    queryset = CustomUser.objects.all()
    pagination_class = CustomPagination

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def subscriptions(self, request):
        queryset = CustomUser.objects.filter(following__user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = FollowSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['post', 'delete'])
    def subscribe(self, request, id):
        return self.add_del(request, Follow, FollowerSerializer, id, True)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None
    http_method_names = ['get']
    filter_backends = [IngredientFilter]
    search_fields = ['^name']


class RecipeViewSet(viewsets.ModelViewSet, AddDelMixin):
    serializer_class = RecipeSerializer
    mixin_serializer = ListRecipeSerializer
    model_class = Recipe
    queryset = Recipe.objects.all().order_by('-id')
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrAuthor]
    pagination_class = CustomPagination
    filterset_class = RecipeFilter

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        return self.add_del(request, Favorite, FavoriteSerializer, pk)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        return self.add_del(request, ShoppingCart, ShoppingCartSerializer, pk)

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        shopping_list = RecipeIngredient.objects.filter(
            recipe__cart_recipe__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).order_by('ingredient__name').annotate(Sum('amount'))
        return generate_pdf(shopping_list)


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None
