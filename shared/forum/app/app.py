import os
import json


def clear_state() -> None:
    """ Функция удаляющая файл состояния (при первом запуске и при выходе пользователя) """
    try:
        os.remove(os.path.join(os.getcwd(), "app", "app.json"))
    except FileNotFoundError:
        pass


def get_state() -> dict:
    """ Функция получающая наше состояние (если файл еще не создан вернем пустой словарь) """
    try:
        with open(os.path.join(os.getcwd(), "app", "app.json"), encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_state(key: str = '', value = None) -> None:
    """ Функция записывающая данные в состояние по ключу с передачей значения """
    data = get_state()

    if key and value:
        data[key] = value
    with open(os.path.join(os.getcwd(), "app", "app.json"), 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
