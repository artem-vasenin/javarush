import datetime as dt

FORMAT = '%H:%M:%S'
WEIGHT = 75  # Вес.
HEIGHT = 175  # Рост.
K_1 = 0.035  # Коэффициент для подсчета калорий.
K_2 = 0.029  # Коэффициент для подсчета калорий.
STEP_M = 0.65  # Длина шага в метрах.

storage_data = {}


def check_correct_data(data):
    """Проверка корректности полученного пакета."""
    pass


def check_correct_time(time):
    """Проверка корректности параметра времени."""
    pass

def get_step_day(steps):
    """Получить количество пройденных шагов за этот день."""
    pass


def get_distance(steps):
    """Получить дистанцию пройденного пути в км."""
    pass


def get_spent_calories(dist, current_time):
    """Получить значения потраченных калорий."""
    pass


def get_achievement(dist):
    """Получить поздравления за пройденную дистанцию."""
    pass


def show_message(time, steps, dist, calories, achievement):
    pass


def accept_package(data):
    """Обработать пакет данных."""
    pass


package_0 = ('2:00:01', 505)
package_1 = (None, 3211)
package_2 = ('9:36:02', 15000)
package_3 = ('9:36:02', 9000)
package_4 = ('8:01:02', 7600)

accept_package(package_0)
accept_package(package_1)
accept_package(package_2)
accept_package(package_3)
accept_package(package_4)
