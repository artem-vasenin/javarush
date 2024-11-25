import hashlib
from datetime import datetime
import json
import os.path
import re

# Состояние приложения. Пишем сюда данные авторизованного пользователя и всякие флаги
state = {
    'branch': {},
    'route': 0,
    'user': {},
}


def print_list_decorator(length=60, symbol='='):
    """ Декоратор для печати списков. Должен оборачивать функции возвращающие список строк из 1 и более элементов """
    def decorator(func):
        def wrapper(*args, **kwargs):
            lst = func(*args, **kwargs)
            print(symbol * length)
            for i in range(len(lst)):
                print(lst[i])
                print('-' * length) if not i + 1 == len(lst) else None
            print(symbol * length)
        return wrapper
    return decorator


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
        3: 'Личные сообщения',
        4: 'Выход'
    } if state['user'] else {
        1: 'Регистрация',
        2: 'Аутентификация',
        3: 'Просмотр веток форума',
        4: 'Завершить программу'
    }
    for key, value in menu_options.items():
        print(f'{key} ---- {value}')

    if state['user']:
        msgs, err = get_pers_msgs(state['user']['login'])
        if not err:
            not_read = list(filter(lambda x: not x['was_read'], msgs[state['user']['login']]))
            print(f'У вас новых сообщений {len(not_read)}. Всего {len(msgs[state['user']['login']])}.')


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
    """ функция для проверки надежности пароля """
    return re.search("(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])^[a-zA-Z0-9]{6,}$", password)


def crypt_password(password) -> str:
    """ Функция возвращает hash пароля """
    return hashlib.md5(password.encode()).hexdigest()


def return_to_main_menu():
    """ Функция возвращающая главное меню и выбор его пункта """
    state['route'] = 0
    print_menu()
    choose_action()


def register_controller():
    """ Функция регистрации нового пользователя """
    role = 'user'
    login = input("Введите Ваш логин (только латинские буквы в нижнем регистре и цифры): ").strip()
    check, err = check_login(login)
    if not check:
        print(err)
        register_controller()
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

def authentication_controller() -> bool:
    global state
    """
    Функция проверяет наличие логина и соответствие ему хеша пароля пользователя
    В случае совпадения возвращает True
    В случае отсутствия пользователя в базе выводит информацию на экран
    В случае несовпадения хеша пароля выводит информацию на экран
    Обращаю внимание, что текст ошибки должен быть идентичен, чтобы хакер не смог перебирать имена пользователей
    """
    flag = False
    login = None
    data = None
    while not flag:
        login = input("Введите имя пользователя: ")
        data, err = get_user_by_login(login)
        password = input("Введите пароль пользователя: ")
        if data and not err:
            if data['passhash'] == crypt_password(password):
                print('Аутентификация прошла успешно')
                flag = True
            else:
                print('Неверное имя пользователя или пароль')
        else:
            print('Неверное имя пользователя или пароль') #Текст ошибки должен быть идентичен

    state['user']["login"] = login
    state['user']["role"] = data['role']
    print_menu()
    choose_action()
    return flag


def authorization():
    pass

def check_menu_branch(select, count):
    """ функция проверки введенных данный в меню branch  """
    global state

    while True:
        if state['user'] and state['user']["role"] == "admin" and select.isdigit() and int(select)==count+1:
            create_branch()
            break
        elif state['user'] and state['user']["role"] == "admin" and select.isdigit() and int(select)==count+2:
            delete_branches()
            break
        elif select.isdigit() and 0<int(select)<count:
            tema = state["branch"][int(select)]
            state["branch"] = tema
            listing_themes()
            break
        elif select.isdigit() and int(select)==count:
            return_to_main_menu()
            break
        else:
            select = input("Выберите корректный пункт меню: ")


def print_branch():
    """ Функция печатающая меню бранчей """
    count = 1
    contents = os.listdir(os.path.join(os.getcwd(), 'branches'))
    for i in range(len(contents)):
        if os.path.isdir(os.path.join(os.getcwd(), 'branches', contents[i])):
            print(f"{count}. {contents[i]}")
            state["branch"][count] = contents[i]
            count += 1
    print(f"{count}. Назад")
    if state['user'] and state['user']["role"] == "admin":
        print("__________________________")
        print(f"{count + 1}. Добавить новую ветку\n{count + 2}. Удалить действующую ветку")
    return count


def listing_branch_controller():
    """ Функция контроллер для меню бранчей """
    count = print_branch()
    select = input("Выберите пункт меню: ")
    check_menu_branch(select, count)


def get_branches_from_db() -> tuple[dict, str]:
    """ Функция получающая содержание текущей ветки. При успехе возвращает словарь
    при неудаче возвращает пустой словарь и ошибку"""
    users_db = [f for f in os.listdir(os.path.join(os.getcwd(), 'branches', state["branch"], )) if '.json' in f]
    data = {}

    if not len(users_db):
        return data, 'База данных не найдена'

    with open(os.path.join(os.getcwd(), 'branches', state["branch"], 'themes.json'), encoding="utf-8") as file:
        data = json.load(file)

    return (data, '') if data["branch_name"]["themes"] else (data, 'Список тем пуст')


def listing_themes():
    """ функция печатающая список тем в выбранной ветке """
    data, err = get_branches_from_db()
    print(f"\nТемы ветки '{data["branch_name"]["title"]}': ")
    if err:
        print(err)
    else:
        for i in range(len(data["branch_name"]["themes"])):
            print(f"{i+1}. {data["branch_name"]["themes"][i]["title_themes"]}")


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


@print_list_decorator(length=90)
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
    data, err = get_pers_msgs(state['user']['login'])
    print_pers_msgs(data[state['user']['login']] if not err else [], err)


def show_new_pers_messages():
    """ Функция печатающая новые личные сообщения пользователя """
    data, err = get_pers_msgs(state['user']['login'])
    print_pers_msgs(list(filter(lambda x: not x['was_read'], data[state['user']['login']])) if not err else [], err)


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


@print_list_decorator()
def print_users() -> list[str]:
    """ Функция запрашивающая список пользователей и выводящая его на печать. Когда будет присвоение ролей надо ее дописать """
    data, err = get_users_from_db()
    if err:
        return [err]
    else:
        lst = []
        for i in range(data['len']):
            u = data['users'][i]
            blocked = f' blocked: {u["blocked_at"]}' if u['blocked_at'] else ''
            lst.append(f'login: {u["login"]} | role: {u["role"]} | registered: {u["created_at"]}{blocked}')

        return lst



def delete_branches():
    print("Удаляю ветку")

def hacker():
    pass

def finish_program():
    pass

def logout():
    """ Функция очищающая сессию пользователя после выхода. Сюда можно добавлять и другие поля для очистки при выходе """
    state['user'] = {}
    state['route'] = 0


def choose_action():
    """ Функция контроллер приложения. Пользователь выбирает параметр по которому происходит роутинг """
    actions = {
        1: print_users,
        2: listing_branch_controller,
        3: personal_messages_controller,
        4: logout,
    } if state['user'] else {
        1: register_controller,
        2: authentication_controller,
        3: listing_branch_controller,
        4: finish_program,
    }

    select = input("Выберите пункт меню: ")
    result = int(select) if select.isdigit() and 0 < int(select) <= len(actions) else len(actions)
    state['route'] = result
    actions[result]()


return_to_main_menu()
