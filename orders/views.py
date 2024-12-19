from http import HTTPStatus
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from .forms import OrderForm
from .models import Order
from customers.models import Customer


@csrf_exempt
@require_http_methods(['POST'])
def create_order(request):
    """
    Функция для оформления заказа.

    Если покупателя с указанным email нет в системе, мы создаём нового.
    Создаём или обновляем заказ на соответствующего робота.
    """
    form = OrderForm(request.POST)

    if form.is_valid():
        customer, _ = Customer.objects.get_or_create(email=form.cleaned_data['email'])

        order, _ = Order.objects.update_or_create(
            customer=customer,
            robot_serial=form.cleaned_data['robot_serial'],
            defaults={'is_notified': False}
        )

        return JsonResponse(
            {'data': order.to_dict()},
            status=HTTPStatus.CREATED
        )

    return JsonResponse(
        {'message': 'Создание заказа не удалось'},
        status=HTTPStatus.BAD_REQUEST
    )
