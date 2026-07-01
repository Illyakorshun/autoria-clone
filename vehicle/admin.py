from django.contrib import admin
from .models import Vehicle, Favorite, VehicleView

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'year', 'price', 'user', 'is_active', 'is_moderated', 'created_at')
    list_filter = ('brand', 'fuel_type', 'transmission', 'body_type', 'is_active', 'is_moderated')
    search_fields = ('brand', 'model', 'description')
    readonly_fields = ('views', 'favorites', 'created_at', 'updated_at')
    fieldsets = (
        ('Основна інформація', {
            'fields': ('user', 'brand', 'model', 'year', 'price')
        }),
        ('Характеристики', {
            'fields': ('mileage', 'fuel_type', 'transmission', 'body_type', 'drive_type', 'engine_volume', 'engine_power', 'color')
        }),
        ('Стан', {
            'fields': ('is_new', 'has_credit', 'has_accident')
        }),
        ('Опис та фото', {
            'fields': ('description', 'main_image', 'images')
        }),
        ('Статистика', {
            'fields': ('views', 'favorites', 'is_active', 'is_moderated')
        }),
    )

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'vehicle', 'created_at')

@admin.register(VehicleView)
class VehicleViewAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'user', 'ip_address', 'created_at')