from django.db import models


class SiteConfig(models.Model):
    """Налаштування сайту"""
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    description = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = 'site_config'

    def __str__(self):
        return self.key


class Contact(models.Model):
    """Зворотній зв'язок"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)

    class Meta:
        db_table = 'contacts'

    def __str__(self):
        return f"{self.name} - {self.email}"