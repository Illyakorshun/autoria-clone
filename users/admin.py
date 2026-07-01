from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'phone', 'is_admin', 'is_active')
    list_filter = ('is_admin', 'is_active', 'created_at')
    search_fields = ('email', 'username', 'first_name', 'last_name', 'phone')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Особиста інформація', {'fields': ('username', 'first_name', 'last_name', 'phone', 'city', 'avatar')}),
        ('Права доступу',
         {'fields': ('is_admin', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Дата', {'fields': ('last_login', 'created_at')}),
    )
    readonly_fields = ('created_at',)