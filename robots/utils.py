from django.utils import timezone
import datetime


def calculate_days_from_today(days: int) -> datetime.date:
    """Функция для получения даты <days> дней назад."""
    return timezone.now().date() - datetime.timedelta(days=days)
