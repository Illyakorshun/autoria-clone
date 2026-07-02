#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autoria.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

    from users.models import User

    # Знаходимо користувача по email
    user = User.objects.get(email='korsillua@gmail.com')

    # Встановлюємо новий пароль
    user.set_password('admin123')
    user.save()

    print(f"✅ Пароль змінено для {user.email}")
    print(f"🔑 Новий пароль: admin123")

    # Перевіряємо чи все ок
    exit()

    from users.models import User

    users = User.objects.all()
    print(f"📊 Всього користувачів: {users.count()}")
    for u in users:
        print(f"Email: {u.email}, Username: {u.username}")
    exit()