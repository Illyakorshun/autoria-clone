from django import template

register = template.Library()

@register.filter
def usd_to_uah(value):
    """Переводить долари в гривні по курсу 41.5"""
    if value is None:
        return 0
    try:
        rate = 41.5
        return int(float(value) * rate)
    except (ValueError, TypeError):
        return value

@register.filter
def format_price(value):
    """Форматує ціну з пробілами"""
    if value is None:
        return '0'
    try:
        return f"{int(float(value)):,}".replace(',', ' ')
    except (ValueError, TypeError):
        return value