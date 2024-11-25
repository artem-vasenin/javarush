import os.path
import json

def get_users_from_db() -> tuple[dict, str]:
    """ Функция получающая всех пользователей из базы. При успехе возвращает словарь с полями
    {users: [{...}], len: int}
    при неудаче возвращает пустой словарь и ошибку"""
    users_db = [f for f in os.listdir(os.path.join(os.getcwd(), 'users', )) if '.json' in f]
    data = {}

    if not len(users_db):
        return data, 'База данных не найдена'

    with open(os.path.join(os.getcwd(), 'users', 'users.json'), encoding="utf-8") as file:
        data = json.load(file)

    return (data, '') if data else (data, 'Список пользователей пуст')