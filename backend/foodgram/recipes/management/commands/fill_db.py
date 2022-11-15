import json

from django.conf import settings
from django.core.management.base import BaseCommand
from recipes.models import Ingredient, Tag


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open(f'{settings.BASE_DIR}/data/ingredients.json', 'rb') as f:
            data = json.load(f)
            for value in data:
                ingredient = Ingredient()
                ingredient.name = value['name']
                ingredient.measurement_unit = value['measurement_unit']
                ingredient.save()

        with open(f'{settings.BASE_DIR}/data/tags.json', 'rb') as f:
            data = json.load(f)
            for value in data:
                tag = Tag()
                tag.name = value['name']
                tag.color = value['color']
                tag.slug = value['slug']
                tag.save()

        print('Filling database complete.')
