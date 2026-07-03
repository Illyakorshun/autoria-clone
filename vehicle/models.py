from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Vehicle(models.Model):
    """Модель автомобіля"""

    FUEL_TYPES = [
        ('BENZIN', 'Бензин'),
        ('DIESEL', 'Дизель'),
        ('ELECTRO', 'Електро'),
        ('HYBRID', 'Гібрид'),
        ('GAS', 'Газ'),
    ]

    TRANSMISSION_TYPES = [
        ('MANUAL', 'Механіка'),
        ('AUTOMATIC', 'Автомат'),
        ('ROBOT', 'Робот'),
        ('CVT', 'Варіатор'),
    ]

    BODY_TYPES = [
        ('SEDAN', 'Седан'),
        ('HATCHBACK', 'Хетчбек'),
        ('SUV', 'Позашляховик'),
        ('COUPE', 'Купе'),
        ('CONVERTIBLE', 'Кабріолет'),
        ('WAGON', 'Універсал'),
        ('MINIVAN', 'Мінівен'),
        ('PICKUP', 'Пікап'),
    ]

    DRIVE_TYPES = [
        ('FRONT', 'Передній'),
        ('REAR', 'Задній'),
        ('FULL', 'Повний'),
    ]

    # ===== Основна інформація =====
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicles')
    brand = models.CharField(max_length=50, verbose_name='Бренд')
    model = models.CharField(max_length=50, verbose_name='Модель')
    year = models.IntegerField(verbose_name='Рік випуску')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Ціна')

    # ===== Характеристики =====
    mileage = models.IntegerField(null=True, blank=True, verbose_name='Пробіг (км)')
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPES, default='BENZIN', verbose_name='Паливо')
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_TYPES, default='MANUAL', verbose_name='Коробка')
    body_type = models.CharField(max_length=20, choices=BODY_TYPES, default='SEDAN', verbose_name='Кузов')
    drive_type = models.CharField(max_length=20, choices=DRIVE_TYPES, default='FRONT', verbose_name='Привід')
    engine_volume = models.FloatField(null=True, blank=True, verbose_name="Об'єм двигуна (л)")
    engine_power = models.IntegerField(null=True, blank=True, verbose_name='Потужність (к.с.)')
    color = models.CharField(max_length=30, null=True, blank=True, verbose_name='Колір')

    # ===== VIN та історія =====
    vin_code = models.CharField(max_length=17, blank=True, null=True, verbose_name='VIN-код')
    owners_count = models.IntegerField(default=1, verbose_name='Кількість власників')
    imported_from = models.CharField(max_length=50, blank=True, null=True, verbose_name='Пригнано з')
    has_accident = models.BooleanField(default=False, verbose_name='Був у ДТП')

    # ===== Стан авто =====
    is_new = models.BooleanField(default=False, verbose_name='Нове')
    has_credit = models.BooleanField(default=False, verbose_name='В кредиті')
    is_trade = models.BooleanField(default=False, verbose_name='Можливий обмін')

    # ===== Опис =====
    description = models.TextField(null=True, blank=True, verbose_name='Опис')

    # ===== Фото =====
    main_image = models.ImageField(upload_to='cars/', null=True, blank=True, verbose_name='Головне фото')

    # ===== Статистика =====
    views = models.IntegerField(default=0, verbose_name='Перегляди')
    favorites = models.IntegerField(default=0, verbose_name='В обраних')

    # ===== Дати =====
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')
    is_active = models.BooleanField(default=True, verbose_name='Активне')
    is_moderated = models.BooleanField(default=False, verbose_name='Пройшло модерацію')

    class Meta:
        db_table = 'vehicles'
        verbose_name = 'Автомобіль'
        verbose_name_plural = 'Автомобілі'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"

    def get_main_image_url(self):
        if self.main_image:
            return self.main_image.url
        return '/static/images/no-image.png'

    def get_all_images(self):
        """Отримує всі фото (головне + додаткові)"""
        images = []
        if self.main_image:
            images.append({
                'url': self.main_image.url,
                'is_main': True
            })
        # Використовуємо related_name='images'
        for img in self.images.all().order_by('order'):
            images.append({
                'url': img.image.url,
                'is_main': False
            })
        return images

    def to_dict(self):
        return {
            'id': self.id,
            'brand': self.brand,
            'model': self.model,
            'year': self.year,
            'price': float(self.price),
            'mileage': self.mileage,
            'fuel_type': self.get_fuel_type_display(),
            'transmission': self.get_transmission_display(),
            'body_type': self.get_body_type_display(),
            'drive_type': self.get_drive_type_display(),
            'engine_volume': self.engine_volume,
            'engine_power': self.engine_power,
            'color': self.color,
            'vin_code': self.vin_code,
            'owners_count': self.owners_count,
            'has_accident': self.has_accident,
            'imported_from': self.imported_from,
            'description': self.description,
            'main_image': self.get_main_image_url(),
            'views': self.views,
            'favorites': self.favorites,
            'created_at': self.created_at.strftime('%d.%m.%Y'),
            'user': {
                'id': self.user.id,
                'name': self.user.get_full_name(),
                'phone': self.user.phone,
                'city': self.user.city,
            }
        }


class VehicleImage(models.Model):
    """Додаткові фото автомобіля"""
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='cars/')
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'vehicle_images'
        ordering = ['order']
        verbose_name = 'Фото автомобіля'
        verbose_name_plural = 'Фото автомобілів'

    def __str__(self):
        return f"Фото для {self.vehicle.brand} {self.vehicle.model}"


class Favorite(models.Model):
    """Модель обраних авто"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_vehicles')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'favorites'
        unique_together = ['user', 'vehicle']
        verbose_name = 'Обране авто'
        verbose_name_plural = 'Обрані авто'

    def __str__(self):
        return f"{self.user.email} -> {self.vehicle}"


class VehicleView(models.Model):
    """Модель переглядів авто"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='views_data')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'vehicle_views'
        verbose_name = 'Перегляд авто'
        verbose_name_plural = 'Перегляди авто'

    def __str__(self):
        return f"{self.vehicle} - {self.created_at}"