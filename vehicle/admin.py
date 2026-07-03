from django.contrib import admin
from .models import Vehicle, VehicleImage, Favorite, VehicleView

class VehicleImageInline(admin.TabularInline):
    """Вбудоване редагування фото"""
    model = VehicleImage
    extra = 3
    fields = ('image', 'order')
    max_num = 10

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    inlines = [VehicleImageInline]
    list_display = ('brand', 'model', 'year', 'price', 'user', 'is_active', 'is_moderated', 'created_at')
    list_filter = ('brand', 'fuel_type', 'transmission', 'body_type', 'is_active', 'is_moderated', 'is_new')
    search_fields = ('brand', 'model', 'description', 'vin_code')
    readonly_fields = ('views', 'favorites', 'created_at', 'updated_at')
    fieldsets = (
        ('Основна інформація', {
            'fields': ('user', 'brand', 'model', 'year', 'price')
        }),
        ('Характеристики', {
            'fields': ('mileage', 'fuel_type', 'transmission', 'body_type', 'drive_type', 'engine_volume', 'engine_power', 'color')
        }),
        ('VIN та історія', {
            'fields': ('vin_code', 'owners_count', 'imported_from', 'has_accident')
        }),
        ('Стан', {
            'fields': ('is_new', 'has_credit', 'is_trade')
        }),
        ('Опис та фото', {
            'fields': ('description', 'main_image')  # ПРИБРАЛИ 'images'
        }),
        ('Статистика', {
            'fields': ('views', 'favorites', 'is_active', 'is_moderated')
        }),
        ('Дата', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'vehicle', 'created_at')
    search_fields = ('user__email', 'vehicle__brand', 'vehicle__model')

@admin.register(VehicleView)
class VehicleViewAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'user', 'ip_address', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('vehicle__brand', 'vehicle__model')