from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from .models import User
import json


def auth_page(request):
    """Сторінка авторизації"""
    if request.user.is_authenticated:
        return redirect('main_app:index')
    return render(request, 'pages/authPage.html')


@login_required
def user_cabinet(request):
    """Особистий кабінет користувача"""
    return render(request, 'pages/userCabinet.html', {
        'user_data': request.user.to_dict()
    })


@login_required
def profile(request):
    """Профіль користувача"""
    return render(request, 'pages/profile.html', {
        'user': request.user
    })


@login_required
@csrf_exempt
def api_profile(request):
    """API - отримання профілю"""
    return JsonResponse({
        'success': True,
        'data': request.user.to_dict()
    })


@login_required
@csrf_exempt
def api_update_profile(request):
    """API - оновлення профілю"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Метод не дозволений'}, status=405)

    try:
        user = request.user
        data = json.loads(request.body)

        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.phone = data.get('phone', user.phone)
        user.city = data.get('city', user.city)

        user.save()

        return JsonResponse({
            'success': True,
            'message': 'Профіль оновлено',
            'data': user.to_dict()
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@login_required
def api_favorites(request):
    """API - отримання обраних авто"""
    # Vehicle models будуть додані пізніше
    return JsonResponse({
        'success': True,
        'data': []
    })


# Пайплайн для Google Auth
def save_profile(backend, user, response, *args, **kwargs):
    """Зберігає додаткові дані з Google"""
    if backend.name == 'google-oauth2':
        user.first_name = response.get('given_name', '')
        user.last_name = response.get('family_name', '')
        if response.get('picture'):
            user.avatar = response.get('picture')
        user.save()