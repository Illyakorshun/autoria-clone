from django.shortcuts import render
from django.http import JsonResponse
from vehicle.models import Vehicle
from django.db.models import Count


def index(request):
    """Головна сторінка"""
    # Останні додані авто
    latest_vehicles = Vehicle.objects.filter(
        is_active=True,
        is_moderated=True
    ).order_by('-created_at')[:8]

    # Якщо немає - показуємо всі
    if not latest_vehicles.exists():
        latest_vehicles = Vehicle.objects.all().order_by('-created_at')[:8]

    # Популярні авто
    popular_vehicles = Vehicle.objects.filter(
        is_active=True,
        is_moderated=True
    ).order_by('-views')[:8]

    if not popular_vehicles.exists():
        popular_vehicles = Vehicle.objects.all().order_by('-views')[:8]

    # Статистика
    stats = {
        'total': Vehicle.objects.filter(is_active=True, is_moderated=True).count(),
        'brands': Vehicle.objects.values('brand').distinct().count(),
        'models': Vehicle.objects.values('model').distinct().count(),
    }

    if stats['total'] == 0:
        stats['total'] = Vehicle.objects.count()
        stats['brands'] = Vehicle.objects.values('brand').distinct().count()
        stats['models'] = Vehicle.objects.values('model').distinct().count()

    # ТУТ ГОЛОВНЕ - рендеримо home.html
    return render(request, 'pages/home.html', {
        'latest_vehicles': latest_vehicles,
        'popular_vehicles': popular_vehicles,
        'stats': stats,
        'title': 'Auto.Ria - Головна'
    })


def about(request):
    return render(request, 'pages/about.html')


def contacts(request):
    return render(request, 'pages/contacts.html')


def api_stats(request):
    return JsonResponse({
        'success': True,
        'data': {
            'total_vehicles': Vehicle.objects.filter(is_active=True).count(),
            'total_users': 0,
            'today_views': 0,
        }
    })


def error_404(request, exception):
    return render(request, 'pages/404.html', status=404)


def error_500(request):
    return render(request, 'pages/500.html', status=500)