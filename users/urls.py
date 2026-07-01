from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Сторінки
    path('cabinet/', views.user_cabinet, name='user_cabinet'),
    path('auth/', views.auth_page, name='auth_page'),
    path('profile/', views.profile, name='profile'),

    # API
    path('api/profile/', views.api_profile, name='api_profile'),
    path('api/update/', views.api_update_profile, name='api_update_profile'),
    path('api/favorites/', views.api_favorites, name='api_favorites'),
]