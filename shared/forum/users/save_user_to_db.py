import json
import os.path
from .get_users_from_db import get_users_from_db

def save_user_to_db(user: dict) -> None:
    """ Функция записи пользователя в базу данных """
    data, error = get_users_from_db()

    if error and not data:
        data['users'] = [user]
        data['len'] = 1
    else:
        data['users'].append(user)
        data['len'] = len(data['users'])

    with open(os.path.join(os.getcwd(), 'users', "users.json"), 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)