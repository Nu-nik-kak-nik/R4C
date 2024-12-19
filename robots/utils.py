import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone


def calculate_days_from_today(days: int) -> datetime.date:
    """Функция для получения даты <days> дней назад."""
    return timezone.now().date() - datetime.timedelta(days=days)


def notify_customers(
        emails: list[str], robot_model: str, robot_version: str
) -> None:
    """
    Функция для отправки email списку получателей.

    В файле R4C/settings.py должны быть заданы следующие переменные:
    - EMAIL_HOST
    - EMAIL_PORT
    - EMAIL_USE_SSL
    - EMAIL_HOST_USER
    - EMAIL_HOST_PASSWORD
    """
    message = f"""
    Добрый день!
    Недавно вы интересовались нашим роботом модели {robot_model}, версии {robot_version}.
    Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами
    """
    send_mail(
        subject='Робот в наличии!',
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=emails,
        fail_silently=False
    )
