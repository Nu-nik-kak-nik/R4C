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


class Model(models.Model):
    """Модель представления модели робота"""
    name = models.CharField(max_length=2, blank=False, null=False)

    def __str__(self) -> str:
        return f"{self.name}"


class Version(models.Model):
    """Модель представления версии модели робота"""
    name = models.CharField(max_length=2, blank=False, null=False)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name}"
