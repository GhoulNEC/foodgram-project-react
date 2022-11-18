import json

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient, Tag


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open(f'{settings.BASE_DIR}/data/ingredients.json', 'rb') as f:
            data = json.load(f)
            for value in data:
                obj, created = Ingredient.objects.get_or_create(
                    name=value['name'],
                    measurement_unit=value['measurement_unit']
                )
                if created:
                    print(f'Ингредиент {value["name"]} '
                          f'{value["measurement_unit"]} добавлен!')
                else:
                    print(f'Ингредиент {value["name"]} '
                          f'{value["measurement_unit"]} уже есть в базе!')

        with open(f'{settings.BASE_DIR}/data/tags.json', 'rb') as f:
            data = json.load(f)
            for value in data:
                obj, created = Tag.objects.get_or_create(
                    name=value['name'],
                    color=value['color'],
                    slug=value['slug']
                )
                if created:
                    print(f'Тег {value["name"]} '
                          f'{value["color"]} {value["slug"]} добавлен!')
                else:
                    print(f'Тег {value["name"]} '
                          f'{value["color"]} {value["slug"]} уже есть в базе!')

        print('Заполнение прошло успешно!')
