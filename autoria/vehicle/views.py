from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import Vehicle, Favorite
import json
import os


def vehicle_list(request):
    """Список всіх авто"""
    vehicles = Vehicle.objects.filter(is_active=True, is_moderated=True)

    # Фільтри
    brand = request.GET.get('brand')
    model = request.GET.get('model')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    year = request.GET.get('year')
    fuel_type = request.GET.get('fuel_type')
    transmission = request.GET.get('transmission')

    if brand:
        vehicles = vehicles.filter(brand__icontains=brand)
    if model:
        vehicles = vehicles.filter(model__icontains=model)
    if min_price:
        vehicles = vehicles.filter(price__gte=min_price)
    if max_price:
        vehicles = vehicles.filter(price__lte=max_price)
    if year:
        vehicles = vehicles.filter(year=year)
    if fuel_type:
        vehicles = vehicles.filter(fuel_type=fuel_type)
    if transmission:
        vehicles = vehicles.filter(transmission=transmission)

    # Пагінація
    paginator = Paginator(vehicles, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Отримуємо всі бренди для фільтрів
    brands = Vehicle.objects.values_list('brand', flat=True).distinct()
    years = Vehicle.objects.values_list('year', flat=True).distinct().order_by('-year')

    return render(request, 'pages/vehicleAdvertisement.html', {
        'vehicles': page_obj,
        'brands': brands,
        'years': years,
        'filters': {
            'brand': brand,
            'model': model,
            'min_price': min_price,
            'max_price': max_price,
            'year': year,
            'fuel_type': fuel_type,
            'transmission': transmission,
        }
    })


def vehicle_detail(request, pk):
    """Детальна сторінка авто"""
    vehicle = get_object_or_404(Vehicle, pk=pk, is_active=True)

    # Збільшуємо кількість переглядів
    vehicle.views += 1
    vehicle.save()

    # Перевіряємо чи в обраних
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, vehicle=vehicle).exists()

    return render(request, 'pages/vehicle_detail.html', {
        'vehicle': vehicle,
        'is_favorite': is_favorite,
    })


def vehicle_search(request):
    """Пошук авто"""
    query = request.GET.get('q', '')
    vehicles = Vehicle.objects.filter(
        Q(brand__icontains=query) |
        Q(model__icontains=query) |
        Q(description__icontains=query),
        is_active=True,
        is_moderated=True
    )

    return render(request, 'pages/searchAdvertisement.html', {
        'vehicles': vehicles,
        'query': query,
    })


@login_required
def liked_vehicles(request):
    """Обрані авто користувача"""
    favorites = Favorite.objects.filter(user=request.user).select_related('vehicle')
    vehicles = [fav.vehicle for fav in favorites if fav.vehicle.is_active]

    return render(request, 'pages/liked.html', {
        'vehicles': vehicles,
    })


@login_required
def add_vehicle(request):
    """Додавання нового авто"""
    if request.method == 'POST':
        try:
            vehicle = Vehicle()
            vehicle.user = request.user
            vehicle.brand = request.POST.get('brand')
            vehicle.model = request.POST.get('model')
            vehicle.year = int(request.POST.get('year'))
            vehicle.price = float(request.POST.get('price'))
            vehicle.mileage = int(request.POST.get('mileage')) if request.POST.get('mileage') else None
            vehicle.fuel_type = request.POST.get('fuel_type')
            vehicle.transmission = request.POST.get('transmission')
            vehicle.body_type = request.POST.get('body_type')
            vehicle.drive_type = request.POST.get('drive_type')
            vehicle.engine_volume = float(request.POST.get('engine_volume')) if request.POST.get(
                'engine_volume') else None
            vehicle.engine_power = int(request.POST.get('engine_power')) if request.POST.get('engine_power') else None
            vehicle.color = request.POST.get('color')
            vehicle.description = request.POST.get('description')

            # Обробка фото
            if request.FILES.get('main_image'):
                vehicle.main_image = request.FILES['main_image']

            vehicle.save()

            messages.success(request, 'Автомобіль додано успішно!')
            return redirect('vehicle:vehicle_detail', pk=vehicle.id)
        except Exception as e:
            messages.error(request, f'Помилка: {str(e)}')

    return render(request, 'pages/add_vehicle.html')


@login_required
def edit_vehicle(request, pk):
    """Редагування авто"""
    vehicle = get_object_or_404(Vehicle, pk=pk, user=request.user)

    if request.method == 'POST':
        try:
            vehicle.brand = request.POST.get('brand')
            vehicle.model = request.POST.get('model')
            vehicle.year = int(request.POST.get('year'))
            vehicle.price = float(request.POST.get('price'))
            vehicle.mileage = int(request.POST.get('mileage')) if request.POST.get('mileage') else None
            vehicle.fuel_type = request.POST.get('fuel_type')
            vehicle.transmission = request.POST.get('transmission')
            vehicle.body_type = request.POST.get('body_type')
            vehicle.drive_type = request.POST.get('drive_type')
            vehicle.engine_volume = float(request.POST.get('engine_volume')) if request.POST.get(
                'engine_volume') else None
            vehicle.engine_power = int(request.POST.get('engine_power')) if request.POST.get('engine_power') else None
            vehicle.color = request.POST.get('color')
            vehicle.description = request.POST.get('description')

            if request.FILES.get('main_image'):
                vehicle.main_image = request.FILES['main_image']

            vehicle.save()
            messages.success(request, 'Оновлено успішно!')
            return redirect('vehicle:vehicle_detail', pk=vehicle.id)
        except Exception as e:
            messages.error(request, f'Помилка: {str(e)}')

    return render(request, 'pages/edit_vehicle.html', {'vehicle': vehicle})


@login_required
def delete_vehicle(request, pk):
    """Видалення авто"""
    vehicle = get_object_or_404(Vehicle, pk=pk, user=request.user)
    if request.method == 'POST':
        vehicle.delete()
        messages.success(request, 'Автомобіль видалено')
        return redirect('main_app:index')
    return redirect('vehicle:vehicle_detail', pk=pk)


# ==================== API ====================

def api_vehicle_list(request):
    """API - список авто"""
    vehicles = Vehicle.objects.filter(is_active=True, is_moderated=True)

    # Фільтри
    brand = request.GET.get('brand')
    model = request.GET.get('model')
    if brand:
        vehicles = vehicles.filter(brand__icontains=brand)
    if model:
        vehicles = vehicles.filter(model__icontains=model)

    data = [v.to_dict() for v in vehicles]
    return JsonResponse({
        'success': True,
        'data': data,
        'count': len(data)
    })


def api_vehicle_detail(request, pk):
    """API - деталі авто"""
    vehicle = get_object_or_404(Vehicle, pk=pk)
    return JsonResponse({
        'success': True,
        'data': vehicle.to_dict()
    })


@login_required
@csrf_exempt
def api_toggle_favorite(request, pk):
    """API - додати/видалити з обраного"""
    vehicle = get_object_or_404(Vehicle, pk=pk)

    favorite = Favorite.objects.filter(user=request.user, vehicle=vehicle)
    if favorite.exists():
        favorite.delete()
        vehicle.favorites -= 1
        vehicle.save()
        return JsonResponse({
            'success': True,
            'is_favorite': False,
            'message': 'Видалено з обраного'
        })
    else:
        Favorite.objects.create(user=request.user, vehicle=vehicle)
        vehicle.favorites += 1
        vehicle.save()
        return JsonResponse({
            'success': True,
            'is_favorite': True,
            'message': 'Додано до обраного'
        })


def api_brands(request):
    """API - список брендів"""
    brands = Vehicle.objects.values_list('brand', flat=True).distinct()
    return JsonResponse({
        'success': True,
        'data': list(brands)
    })


@csrf_exempt
def api_load_data(request):
    """API - завантаження тестових даних з JSON"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Метод не дозволений'}, status=405)

    try:
        import json
        from django.contrib.auth import get_user_model
        User = get_user_model()

        # Отримуємо адміна
        admin = User.objects.filter(is_admin=True).first()
        if not admin:
            return JsonResponse({'error': 'Адміна не знайдено'}, status=404)

        # Читаємо JSON
        json_path = os.path.join(os.path.dirname(__file__), 'assets', 'cars.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            cars_data = json.load(f)

        count = 0
        for car_data in cars_data:
            car = Vehicle.objects.create(
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

        return JsonResponse({
            'success': True,
            'message': f'Завантажено {count} авто'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)