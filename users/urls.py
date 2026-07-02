from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('authPage/', views.auth_page, name='auth_page'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('cabinet/', views.user_cabinet, name='user_cabinet'),
    path('adminPanel/', views.admin_panel, name='admin_panel'),
    path('liked/', views.liked_vehicles, name='liked_vehicles'),
    path('profile/', views.profile, name='profile'),
    path('api/profile/', views.api_profile, name='api_profile'),
    path('api/update/', views.api_update_profile, name='api_update_profile'),
    path('api/favorites/', views.api_favorites, name='api_favorites'),
    path('api/google-login/', views.api_google_login, name='api_google_login'),

]