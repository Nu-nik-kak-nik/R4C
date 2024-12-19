import re


def validate_robot_data(robot_data: dict) -> bool:
    """Валидация данных о произведенных на заводе роботах"""
    pattern = re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')
    attributes = ('model', 'version', 'created')

    if not pattern.match(str(robot_data.get('created'))):
        return False

    for attribute in attributes:

        if not robot_data.get(attribute):
            return False

    return True
