from django.db import models


class Robot(models.Model):
    """Модель роботов, созданных на заводе"""
    serial = models.CharField(max_length=5, blank=False, null=False)
    model = models.CharField(max_length=2, blank=False, null=False)
    version = models.CharField(max_length=2, blank=False, null=False)
    created = models.DateTimeField(blank=False, null=False)
    is_available = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.model}-{self.version}"
