import os
import json
from datetime import datetime

import shared.forum.utils.utils as ut
import shared.forum.users.user as user
import shared.forum.app.status as status


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


def save_personal_msg_to_db(login: str, msg: str)-> tuple[str, str]:
    """ Сохранение нового сообщения для пользователя в базу данных """
    msgs, msgs_err = get_pers_msgs()

    item = {
        'from': status.statu.stat['user']['login'],
        'message': msg,
        'was_read': False,
        'was_answered': False,
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    msgs[login] = [item] if (not msgs and msgs_err) or login not in msgs else [*msgs[login], item]

    with open(os.path.join(os.getcwd(), "messages", "messages.json"), 'w', encoding="utf-8") as file:
        json.dump(msgs, file, indent=2, ensure_ascii=False)

    return 'Сообщение успешно отправлено', ''


def send_personal_message():
    """ Функция контроллер для работы с сообщениями пользователя """
    login = input('Введите логин адресата: ')
    _, login_err = user.get_user_by_login(login)

    if login_err:
        print(login_err)
        send_personal_message()
        return

    msg = input('Ваше сообщение: ')
    while len(msg.strip()) < 6:
        msg = input('Хорош баловаться, введите сообщение: ')
    result_msg, save_err = save_personal_msg_to_db(login, msg)

    print(save_err if save_err else result_msg)


@ut.print_list_decorator(length=90)
def print_pers_msgs(lst: list, err) -> list[str]:
    """ Функция оформляющая список сообщений перед выводом """
    if err:
        return [err]
    else:
        if len(lst):
            return [f'Отправитель: {x['from'].ljust(10)} | Дата: {x['created_at']} | "{x['message']}"' for x in lst]
        else:
            return ['Сообщений пока нет']


def show_all_pers_messages():
    """ Функция печатающая все личные сообщения пользователя """
    data, err = get_pers_msgs(status.statu.stat['user']['login'])
    print_pers_msgs(data[status.statu.stat['user']['login']] if not err else [], err)


def show_new_pers_messages():
    """ Функция печатающая новые личные сообщения пользователя """
    data, err = get_pers_msgs(status.statu.stat['user']['login'])
    print_pers_msgs(list(filter(lambda x: not x['was_read'], data[status.statu.stat['user']['login']])) if not err else [], err)


def personal_messages(cb):
    """ Функция-контроллер для функционала личных сообщений """
    actions = {
        1: {'title': 'Показать все сообщения', 'action': show_all_pers_messages},
        2: {'title': 'Показать непрочитанные сообщения', 'action': show_new_pers_messages},
        3: {'title': 'Написать личное сообщение', 'action': send_personal_message},
        4: {'title': 'Выйти в главное меню', 'action': None},
    }
    print(*[f'{k}: {v['title']}' for k, v in actions.items()], sep='\n')

    def check(val: str) -> bool:
        return val.isdigit() and 0 < int(val) < 5

    res = input('Сообщения. Выберите пункт меню: ')
    while not check(res):
        res = input('Сообщения. Выберите пункт меню. Опять...: ')

    if int(res) == 4:
        cb()
        return

    actions[int(res)]['action']()