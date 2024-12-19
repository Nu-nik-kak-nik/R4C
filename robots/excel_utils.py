import os
import xlsxwriter
from django.conf import settings


def create_production_list(robots) -> str:
    """
    Функция для создания xlsx файла со сводной
    информацией о произведенных роботах.
    """
    dict_robots = {}
    for robot in robots:
        model_version = f"{robot['model']}-{robot['version']}"
        if model_version not in dict_robots:
            dict_robots[model_version] = robot['robot_count']
        else:
            dict_robots[model_version] += robot['robot_count']

    file_path = os.path.join(settings.BASE_DIR, 'production_list', 'robots_list.xlsx')
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    workbook = xlsxwriter.Workbook(file_path)
    worksheet = workbook.add_worksheet(name='Сводка')
    worksheet.write(0, 0, 'Модель-Версия')
    worksheet.write(0, 1, 'Количество за неделю')

    for ind, (model_version, count) in enumerate(dict_robots.items()):
        worksheet.write(ind + 1, 0, model_version)
        worksheet.write(ind + 1, 1, count)

    workbook.close()

    return file_path
