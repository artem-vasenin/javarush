from ..users import get_user_by_login
from .save_personal_msg_to_db import save_personal_msg_to_db

def send_personal_message(login_from: str):
    """ Функция контроллер для работы с сообщениями пользователя """
    login_to = input('Введите логин адресата: ')
    _, login_err = get_user_by_login(login_to)

    if login_err:
        print(login_err)
        send_personal_message(login_from)
        return

    msg = input('Ваше сообщение: ')
    while len(msg.strip()) < 6:
        msg = input('Хорош баловаться, введите сообщение: ')
    result_msg, save_err = save_personal_msg_to_db(login_from, login_to, msg)

    print(save_err if save_err else result_msg)