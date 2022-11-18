from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT


class AddDelMixin:
    model_class = None
    mixin_serializer = None

    def add_del(self, request, model, serializer, pk, is_user_view=False):
        user = request.user
        obj_1 = get_object_or_404(self.model_class, id=pk)
        data = {'author': obj_1.id} if is_user_view else {'recipe': obj_1.id}
        if request.method == 'POST':
            serializer = serializer(
                data=data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            serializer = self.mixin_serializer(obj_1)
            return Response(data=serializer.data, status=HTTP_201_CREATED)
        obj_2 = (get_object_or_404(model, user=user, author=obj_1)
                 if is_user_view
                 else get_object_or_404(model, user=user,
                                        recipe=obj_1))
        obj_2.delete()
        return Response(status=HTTP_204_NO_CONTENT)
