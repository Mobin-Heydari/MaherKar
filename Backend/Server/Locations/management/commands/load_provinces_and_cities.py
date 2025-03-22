import json
from django.core.management.base import BaseCommand
from Locations.models import Province, City  # Import your models
from Server.settings import BASE_DIR
import os

class Command(BaseCommand):
    help = 'Load provinces and cities from a JSON file into the database'

    def handle(self, *args, **kwargs):
        # Correcting the file path by removing square brackets
        with open(os.path.join(BASE_DIR, 'static/json/provinces_and_main_cities.json'), encoding='utf-8') as file:
            data = json.load(file)

        # Loop through provinces and cities
        for province_data in data:
            province, created = Province.objects.get_or_create(name=province_data['name'])
            for city_name in province_data['cities']:
                City.objects.get_or_create(name=city_name, province=province)

        self.stdout.write(self.style.SUCCESS('Successfully loaded provinces and cities!'))
