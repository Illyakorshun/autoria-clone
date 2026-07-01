from vehicle.models import Vehicle

def site_data(request):
    """Глобальні дані для всіх шаблонів"""
    return {
        'site_name': 'Auto.Ria',
        'site_description': 'Продаж автомобілів в Україні',
        'total_cars': Vehicle.objects.filter(is_active=True).count(),
        'current_year': 2024,
    }