from django.urls import path
from . import views

app_name = 'vehicle'

urlpatterns = [
    # Сторінки
    path('', views.vehicle_list, name='vehicle_list'),
    path('<int:pk>/', views.vehicle_detail, name='vehicle_detail'),
    path('search/', views.vehicle_search, name='vehicle_search'),
    path('liked/', views.liked_vehicles, name='liked_vehicles'),
    path('add/', views.add_vehicle, name='add_vehicle'),
    path('<int:pk>/edit/', views.edit_vehicle, name='edit_vehicle'),
    path('<int:pk>/delete/', views.delete_vehicle, name='delete_vehicle'),
    path('', views.vehicle_list, name='vehicle_list'),
    path('search/', views.vehicle_search, name='vehicle_search'),
    path('add/', views.add_vehicle, name='add_vehicle'),
    path('<int:pk>/', views.vehicle_detail, name='vehicle_detail'),
    path('new/', views.vehicle_list, name='new_vehicles'),

    # API
    path('api/list/', views.api_vehicle_list, name='api_vehicle_list'),
    path('api/<int:pk>/', views.api_vehicle_detail, name='api_vehicle_detail'),
    path('api/<int:pk>/favorite/', views.api_toggle_favorite, name='api_toggle_favorite'),
    path('api/brands/', views.api_brands, name='api_brands'),
    path('api/load-data/', views.api_load_data, name='api_load_data'),
]