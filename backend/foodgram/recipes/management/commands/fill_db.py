import json

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient, Tag


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open(f'{settings.BASE_DIR}/data/ingredients.json', 'rb') as f:
            data = json.load(f)
            for value in data:
                success_msg = (f'Ингредиент {value["name"]} '
                               f'{value["measurement_unit"]} добавлен!')
                failure_msg = (f'Ингредиент {value["name"]} '
                               f'{value["measurement_unit"]} уже есть в базе!')
                obj, created = Ingredient.objects.get_or_create(
                    name=value['name'],
                    measurement_unit=value['measurement_unit']
                )
                print(success_msg if created else failure_msg)

        with open(f'{settings.BASE_DIR}/data/tags.json', 'rb') as f:
            data = json.load(f)
            for value in data:
                success_msg = (f'Тег {value["name"]} {value["color"]} '
                               f'{value["slug"]} добавлен!')
                failure_msg = (f'Тег {value["name"]} {value["color"]} '
                               f'{value["slug"]} уже есть в базе!')
                obj, created = Tag.objects.get_or_create(
                    name=value['name'],
                    color=value['color'],
                    slug=value['slug']
                )
                print(success_msg if created else failure_msg)

        print('Заполнение прошло успешно!')
