from .get_user_by_login import get_user_by_login
import re

def check_login(login: str) -> tuple[bool, str]:
    """ Проверка логина пользователя """
    user, err = get_user_by_login(login)
    if not err and user:
        return False, 'Имя пользователя уже занято. Повторите ввод.'
    if len(login) > 3 and re.search("^[a-zA-Z][a-zA-Z0-9]*$", login):
        return True, ''
    else:
        return False, 'Логин введен некорректно. Повторите ввод.'