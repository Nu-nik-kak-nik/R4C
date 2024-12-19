import os
import json
from http import HTTPStatus

from django.http import JsonResponse, HttpResponse, Http404
from django.db.models import Count
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from .models import Robot
from .validators import validate_robot_data
from .utils import calculate_days_from_today
from .excel_utils import create_production_list


@csrf_exempt
def add_robot(request):
    """
        Функция представления для добавления робота.

        Создает робота на основе данных, полученных из запроса.
        Если указанные модель или версия робота не существуют, возвращается 404.
        При успешном добавлении робота проверяются заказы покупателей на него.
        Если такие заказы имеются, заказчикам отправляется уведомление по электронной почте.
    """
    try:
        data = json.loads(request.body)

        if not validate_robot_data(data):
            return JsonResponse(
                {'message': 'Полученные данные не соответствуют ожиданиям'},
                status=HTTPStatus.BAD_REQUEST
            )

        robot = Robot.objects.create(
            serial=f'{data["model"]}-{data["version"]}',
            model=data['model'],
            version=data['version'],
            created=data['created']
        )

        return JsonResponse(
            {'data': {
                'serial': robot.serial,
                'model': robot.model,
                'version': robot.version,
                'created': robot.created.isoformat()
            }},
            status=HTTPStatus.CREATED
        )

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=HTTPStatus.BAD_REQUEST)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=HTTPStatus.BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=HTTPStatus.INTERNAL_SERVER_ERROR)


@require_http_methods(['GET'])
def download_production_list(request):
    """
    Вью функция для получения Excel файла с информацией о
    произведенных роботах за последнюю неделю.
    """
    robots = Robot.objects.filter(
        created__date__gte=calculate_days_from_today(days=7)
    ).values('model', 'version').annotate(robot_count=Count('id'))

    prod_list = create_production_list(robots)

    if os.path.exists(prod_list):
        with open(prod_list, 'rb') as fh:
            response = HttpResponse(
                fh.read(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename=production_list.xlsx'
        return response

    raise Http404("Файл не найден")
