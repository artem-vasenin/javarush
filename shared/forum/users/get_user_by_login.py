from .get_users_from_db import get_users_from_db

def get_user_by_login(login: str) -> tuple[dict, str]:
    """ Функция получающая пользователя из базы по логину, если отсутствует получаем пустой словарь и ошибку """
    data, err = get_users_from_db()

    if err:
        return data, err
    else:
        lst = [x for x in data['users'] if x['login'] == login]
        return (lst[0], '') if lst else ({}, 'Пользователь не найден')