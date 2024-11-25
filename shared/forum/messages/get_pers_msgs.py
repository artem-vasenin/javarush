import json
import os.path

def get_pers_msgs(login: str = '') -> tuple[dict, str]:
    """ Функция получения всех сообщений или сообщений для конкретного пользователя """
    msgs_db = [f for f in os.listdir(os.path.join(os.getcwd(), "messages", )) if '.json' in f]

    if not len(msgs_db):
        return {}, 'База данных не найдена'

    with open(os.path.join(os.getcwd(), 'messages', 'messages.json'), encoding="utf-8") as file:
        response = json.load(file)

        if not response or (login and not login in response):
            return {}, 'Список сообщений пуст'

        return ({login: response[login]}, '') if login else (response, '')