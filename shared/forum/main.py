import hashlib
from datetime import datetime
import json
import os.path
import re

# Состояние приложения. Пишем сюда данные авторизованного пользователя и всякие флаги
state = {
    'route': 0,
    'user': {},
    # 'user': { 'login': 'Artem', 'role': 'admin', 'logged_at': '2024-11-19 10:15:39' },
}


def get_users_from_db() -> tuple[dict, str]:
    """ Функция получающая всех пользователей из базы. При успехе возвращает словарь с полями
    {users: [{...}], len: int}
    при неудаче возвращает пустой словарь и ошибку"""
    users_db = [f for f in os.listdir(os.path.join(os.getcwd(), "users", )) if '.json' in f]
    data = {}

    if not len(users_db):
        return data, 'База данных не найдена'

    with open(os.path.join(os.getcwd(), 'users', 'users.json'), encoding="utf-8") as file:
        data = json.load(file)

    return (data, '') if data else (data, 'Список пользователей пуст')


def get_user_by_login(login: str) -> tuple[dict, str]:
    """ Функция получающая пользователя из базы по логину, если отсутствует получаем пустой словарь и ошибку """
    data, err = get_users_from_db()

    if err:
        return data, err
    else:
        lst = [x for x in data['users'] if x['login'] == login]
        return (lst[0], '') if lst else ({}, 'Пользователь не найден')


def save_user_to_db(user: dict) -> None:
    """ Функция записи пользователя в базу данных """
    data, error = get_users_from_db()

    if error and not data:
        data['users'] = [user]
        data['len'] = 1
    else:
        data['users'].append(user)
        data['len'] = len(data['users'])

    with open(os.path.join(os.getcwd(), "users", "users.json"), 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


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
        'from': state['user']['login'],
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
    menu_options = {
        1: 'Просмотр списка пользователей',
        2: 'Просмотр веток форума',
        3: 'Написать личное сообщение',
        4: 'Выход'
    } if state['user'] else {
        1: 'Регистрация',
        2: 'Аутентификация',
        3: 'Просмотр веток форума',
        4: 'Завершить программу'
    }
    for key, value in menu_options.items():
        print(f'{key} ---- {value}')


def check_login(login: str) -> tuple[bool, str]:
    """ Проверка логина пользователя """
    user, err = get_user_by_login(login)
    if not err and user:
        return False, 'Имя пользователя уже занято. Повторите ввод.'
    if len(login) > 3 and re.search("^[a-zA-Z][a-zA-Z0-9]*$", login):
        return True, ''
    else:
        return False, 'Логин введен некорректно. Повторите ввод.'


def check_password(password):
    # функция для проверки надежности пароля
    return re.search("(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])^[a-zA-Z0-9]{6,}$", password)


def crypt_password(password) -> str:
    """ Функция возвращает hash пароля """
    return hashlib.md5(password.encode()).hexdigest()


def register():
    """ Функция регистрации нового пользователя """
    role = 'user'
    login = input("Введите Ваш логин (только латинские буквы в нижнем регистре и цифры): ").strip()
    check, err = check_login(login)
    if not check:
        print(err)
        register()
        return

    password = input("Введите Ваш пароль: ")
    while not check_password(password):
        password = input("Пароль не безопасный, введите другой: ")

    hash_password = crypt_password(password)
    """ По запросу секретного ключа, если он не верный (не найден среди действующих), может запрашивать у пользователя: 
    "Вы хотите зарегистрироваться как обычный пользователь или админ?" если админ, то просит ввести ключ повторно """
    secretkey = input("Введите секретный ключ (для привилегированных пользователей): ")
    if secretkey == "аз есмь царь!":
        role = 'admin'

    user = {
        'login': login,
        'passhash': hash_password,
        'role': role,
        'blocked_at': '',
        'blocked_reason': '',
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'name': '',
        'city': '',
    }
    save_user_to_db(user)


def write_post():
    pass

def authentication() -> bool:
    global state
    """
    Функция проверяет наличие логина и соответствие ему хеша пароля пользователя
    В случае совпадения возвращает True
    В случае отсутствия пользователя в базе выводит информацию на экран
    В случае несовпадения хеша пароля выводит информацию на экран
    Обращаю внимание, что текст ошибки должен быть идентичен, чтобы хакер не смог перебирать имена пользователей
    """
    flag = False
    while not flag:
        login = input("Введите имя пользователя: ")
        data, err = get_user_by_login(login)
        password = input("Введите пароль пользователя: ")
        # ToDo: можно упростить код если ошибка одинаковая
        if data and not err: # ToDo: здесь просто добавить проверку пароля а все что else неверный логин или пароль
            if data['passhash'] == crypt_password(password):
                print('Аутентификация прошла успешно')
                flag = True
            else:
                print('Неверное имя пользователя или пароль')
        else:
            print('Неверное имя пользователя или пароль') #Текст ошибки должен быть идентичен
    state['user']["login"] = login # ToDo: ошибка. Вне блока while нет переменной login, или создать ее выше или работать в контексте
    state['user']["role"] = data['role'] # ToDo: ошибка. Вне блока while нет переменной data
    print_menu()
    choose_action()
    return flag # ToDo: не забываем о красоте кода, отступах между функциями, условиями и переменными по возможности тоже

def authorization():
    pass


def listing_branch():
    count = 1
    # ToDo: эти проверки и получение списка бранчей я бы вынес в отдельную функцию работающую с базой а тут только получал данные или ошибку
    contents = os.listdir(os.path.join(os.getcwd(), 'branches'))
    for i in range(len(contents)):
        if os.path.isdir(os.path.join(os.getcwd(), 'branches', contents[i])):
            print(f"{count}. {contents[i]}")
            count += 1
    print(f"{count}. Назад")
    if state['user'] and state['user']["role"] == "admin":
        print("__________________________")
        print(f"{count+1}. Добавить новую ветку\n{count + 2}. Удалить действующую ветку")
    select = input("Выберите пункт меню: ")
    # ToDo: старайся не вызывать функции до того как их объявила и описала, тут вроде смотрю они "всплывают"
    # ToDo: но могут быть ошибки в дальнейшем. Лучше чеккеры вынести вверх как и функции работы с базой
    check_menu_branch(select, count)


def check_menu_branch(select, count):
    while True:
        if state['user'] and state['user']["role"] == "admin" and select.isdigit() and int(select)==count+1:
            create_branch()
            break
        elif state['user'] and state['user']["role"] == "admin" and select.isdigit() and int(select)==count+2:
            delete_branches()
            break
        elif select.isdigit() and 0<int(select)<count:
            listing_themes()
            break
        elif select.isdigit() and int(select)==count:
            print_menu()
            choose_action()
            break
        else:
            select = input("Выберите корректный пункт меню: ")


def listing_themes():
    print("Смотрю темы")

def create_branch():
    print("Добавляю ветку")

def create_themes():
    pass

def create_forum_messages():
    pass

def send_personal_message():
    """ Функция контроллер для работы с сообщениями пользователя """
    login = input('Введите логин адресата: ')
    _, login_err = get_user_by_login(login)

    if login_err:
        print(login_err)
        send_personal_message()
        return

    msg = input('Ваше сообщение: ')
    while len(msg.strip()) < 6:
        msg = input('Хорош баловаться, введите сообщение: ')
    result_msg, save_err = save_personal_msg_to_db(login, msg)

    print(save_err if save_err else result_msg)


def bot():
    pass

def block_users():
    pass

def unblock_users():
    pass

def delete_users():
    pass


def print_users() -> None:
    """ Функция запрашивающая список пользователей и выводящая его на печать. Когда будет присвоение ролей надо ее дописать """
    data, err = get_users_from_db()
    print('='*60)

    if err:
        print(err)
    else:
        for i in range(data['len']):
            u = data['users'][i]
            print(f'login: {u["login"]} | role: {u["role"]} | registered: {u["created_at"]}', f'blocked: {u["blocked_at"]}' if u['blocked_at'] else '')
            print('-'*60 if i + 1 < data['len'] else '', end='\n' if i + 1 < data['len'] else '')
    print('='*60)



def delete_branches():
    print("Удаляю ветку")

def hacker():
    pass

def finish_program():
    pass

def logout():
    state['user'] = {}
    state['route'] = 0


def choose_action():
    """ Функция контроллер приложения. Пользователь выбирает параметр по которому происходит роутинг """
    actions = {
        1: print_users,
        2: listing_branch,
        3: send_personal_message,
        4: logout,
    } if state['user'] else {
        1: register,
        2: authentication,
        3: listing_branch,
        4: finish_program,
    }

    select = input("Выберите пункт меню: ")
    result = int(select) if select.isdigit() and 0 < int(select) <= len(actions) else len(actions)
    state['route'] = result
    actions[result]()


print_menu()
choose_action()
