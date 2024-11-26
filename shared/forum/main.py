from datetime import datetime
import json
import os.path

import utils.utils as ut
import users.user as user
import app.app as app
import branches.forum as forum


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
    st = app.get_state()
    msgs, msgs_err = get_pers_msgs()

    item = {
        'from': st['user']['login'],
        'message': msg,
        'was_read': False,
        'was_answered': False,
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    msgs[login] = [item] if (not msgs and msgs_err) or login not in msgs else [*msgs[login], item]

    with open(os.path.join(os.getcwd(), "messages", "messages.json"), 'w', encoding="utf-8") as file:
        json.dump(msgs, file, indent=2, ensure_ascii=False)

    return 'Сообщение успешно отправлено', ''


def print_menu() -> None:
    """ Главное меню приложения """
    st = app.get_state()
    menu_options = {
        1: 'Просмотр списка пользователей',
        2: 'Просмотр веток форума',
        3: 'Личные сообщения',
        4: 'Выход'
    } if st.get('user') else {
        1: 'Регистрация',
        2: 'Аутентификация',
        3: 'Просмотр веток форума',
        4: 'Завершить программу'
    }
    for key, value in menu_options.items():
        print(f'{key} ---- {value}')

    if st.get('user'):
        msgs, err = get_pers_msgs(st['user']['login'])
        if not err:
            not_read = list(filter(lambda x: not x['was_read'], msgs[st['user']['login']]))
            print(f'У вас новых сообщений {len(not_read)}. Всего {len(msgs[st['user']['login']])}.')


def return_to_main_menu():
    """ Функция возвращающая главное меню и выбор его пункта """
    print_menu()
    choose_action()


def authentication_controller():
    """ Вызов функции входа в приложение """
    user.authentication()
    print_menu()
    choose_action()


def register_controller():
    """ Вызов функции регистрации пользователя """
    user.register()
    print_menu()
    choose_action()


def listing_branch_controller():
    """ Функция контроллер для меню бранчей """
    count = forum.print_branch()
    select = input("Выберите пункт меню: ")
    forum.check_menu_branch(select, count)


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
    st = app.get_state()
    data, err = get_pers_msgs(st['user']['login'])
    print_pers_msgs(data[st['user']['login']] if not err else [], err)


def show_new_pers_messages():
    """ Функция печатающая новые личные сообщения пользователя """
    st = app.get_state()
    data, err = get_pers_msgs(st['user']['login'])
    print_pers_msgs(list(filter(lambda x: not x['was_read'], data[st['user']['login']])) if not err else [], err)


def personal_messages_controller():
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
        return_to_main_menu()
        return

    actions[int(res)]['action']()


def bot():
    pass

def block_users():
    pass

def unblock_users():
    pass

def delete_users():
    pass


@ut.print_list_decorator()
def print_users() -> list[str]:
    """ Функция запрашивающая список пользователей и выводящая его на печать. Когда будет присвоение ролей надо ее дописать """
    data, err = user.get_users_from_db()
    if err:
        return [err]
    else:
        lst = []
        for i in range(data['len']):
            u = data['users'][i]
            blocked = f' blocked: {u["blocked_at"]}' if u['blocked_at'] else ''
            lst.append(f'login: {u["login"]} | role: {u["role"]} | registered: {u["created_at"]}{blocked}')

        return lst

def hacker():
    pass

def finish_program():
    pass

def logout():
    """ Функция очищающая сессию пользователя после выхода. Сюда можно добавлять и другие поля для очистки при выходе """
    app.clear_state()


def choose_action():
    """ Функция контроллер приложения. Пользователь выбирает параметр по которому происходит роутинг """
    st = app.get_state()
    actions = {
        1: print_users,
        2: listing_branch_controller,
        3: personal_messages_controller,
        4: logout,
    } if st.get('user') else {
        1: register_controller,
        2: authentication_controller,
        3: listing_branch_controller,
        4: finish_program,
    }

    select = input("Выберите пункт меню: ")
    result = int(select) if select.isdigit() and 0 < int(select) <= len(actions) else len(actions)
    actions[result]()


logout()
return_to_main_menu()
