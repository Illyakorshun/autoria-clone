from django.core.management.base import BaseCommand
from vehicle.models import Vehicle
from django.contrib.auth import get_user_model
import json
import os

User = get_user_model()


class Command(BaseCommand):
    help = 'Завантажує тестові дані авто з JSON файлу'

    def handle(self, *args, **options):
        admin = User.objects.filter(is_admin=True).first()
        if not admin:
            self.stdout.write(self.style.ERROR('Адміна не знайдено!'))
            return

        json_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'cars.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            cars_data = json.load(f)

        count = 0
        for car_data in cars_data:
            Vehicle.objects.create(
                user=admin,
                brand=car_data.get('brand'),
                model=car_data.get('model'),
                year=car_data.get('year'),
                price=car_data.get('price'),
                mileage=car_data.get('mileage'),
                fuel_type=car_data.get('fuel_type', 'BENZIN'),
                transmission=car_data.get('transmission', 'AUTOMATIC'),
                body_type=car_data.get('body_type', 'SEDAN'),
                drive_type=car_data.get('drive_type', 'FRONT'),
                engine_volume=car_data.get('engine_volume'),
                engine_power=car_data.get('engine_power'),
                color=car_data.get('color'),
                description=car_data.get('description'),
                is_moderated=True,
                is_active=True,
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f'Завантажено {count} авто'))