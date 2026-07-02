from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
import json
import requests


def register(request):
    """Реєстрація користувача"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        username = request.POST.get('username', email.split('@')[0] if email else 'user')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')

        if password1 != password2:
            messages.error(request, 'Паролі не співпадають')
            return render(request, 'pages/authPage.html', {'error': 'Паролі не співпадають'})

        if len(password1) < 6:
            messages.error(request, 'Пароль має бути не менше 6 символів')
            return render(request, 'pages/authPage.html', {'error': 'Пароль має бути не менше 6 символів'})

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Користувач з таким email вже існує')
            return render(request, 'pages/authPage.html', {'error': 'Користувач з таким email вже існує'})

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name
            )
            login(request, user)
            messages.success(request, f'Вітаємо, {user.first_name or user.username}!')
            return redirect('/')
        except Exception as e:
            messages.error(request, f'Помилка: {str(e)}')
            return render(request, 'pages/authPage.html', {'error': str(e)})

    return render(request, 'pages/authPage.html')


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # ПРОСТО АУТЕНТИФІКАЦІЯ
        user = authenticate(request, username=email, password=password)

        if user is None:
            # Спробуємо знайти по email
            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(request, username=user_obj.username, password=password)
            except:
                pass

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Неправильний email або пароль')
            return render(request, 'pages/authPage.html', {'error': 'Неправильний email або пароль'})

    return render(request, 'pages/authPage.html')


def user_logout(request):
    """Вихід з системи"""
    logout(request)
    messages.info(request, 'Ви вийшли з системи')
    return redirect('/')


def auth_page(request):
    """Сторінка авторизації"""
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'pages/authPage.html', {
        'google_client_id': '1031078906485-75of6f54vl776korlbcg0kpl18jakd5l.apps.googleusercontent.com'
    })


@login_required
def user_cabinet(request):
    return render(request, 'pages/userCabinet.html', {
        'user_data': request.user.to_dict()
    })


@login_required
def admin_panel(request):
    if not request.user.is_admin:
        messages.error(request, 'Доступ заборонено')
        return redirect('/')
    return render(request, 'pages/adminPanel.html', {
        'user': request.user
    })


@login_required
def liked_vehicles(request):
    from vehicle.models import Favorite
    favorites = Favorite.objects.filter(user=request.user).select_related('vehicle')
    vehicles = [fav.vehicle for fav in favorites if fav.vehicle.is_active]
    return render(request, 'pages/liked.html', {
        'vehicles': vehicles,
    })


@login_required
def profile(request):
    return render(request, 'pages/profile.html', {
        'user': request.user
    })


# ==================== API ====================

@login_required
@csrf_exempt
def api_profile(request):
    return JsonResponse({
        'success': True,
        'data': request.user.to_dict()
    })


@login_required
@csrf_exempt
def api_update_profile(request):
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
    from vehicle.models import Favorite
    favorites = Favorite.objects.filter(user=request.user).select_related('vehicle')
    data = [fav.vehicle.to_dict() for fav in favorites]
    return JsonResponse({
        'success': True,
        'data': data
    })


@csrf_exempt
def api_google_login(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Метод не дозволений'}, status=405)

    try:
        data = json.loads(request.body)
        token = data.get('token')

        if not token:
            return JsonResponse({'error': 'Токен не надано'}, status=400)

        response = requests.get(f'https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={token}')
        user_info = response.json()

        if 'error' in user_info:
            return JsonResponse({'error': 'Невірний токен'}, status=400)

        email = user_info.get('email')
        name = user_info.get('name', '')
        given_name = user_info.get('given_name', '')
        family_name = user_info.get('family_name', '')

        if not email:
            return JsonResponse({'error': 'Email не знайдено'}, status=400)

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': email.split('@')[0],
                'first_name': given_name or name,
                'last_name': family_name,
                'is_active': True,
            }
        )

        if not created:
            if given_name and not user.first_name:
                user.first_name = given_name
            if family_name and not user.last_name:
                user.last_name = family_name
            user.save()

        login(request, user)

        return JsonResponse({
            'success': True,
            'created': created,
            'user': user.to_dict(),
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=400)


def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2':
        user.first_name = response.get('given_name', '')
        user.last_name = response.get('family_name', '')
        if response.get('picture'):
            user.avatar = response.get('picture')
        user.save()