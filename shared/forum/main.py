import hashlib
from datetime import datetime
import json
import os.path
import string

dict_branch = {1: {"Погода":["Опять дождь", "Невыносимая жара", "Мороз"]}, 2:"Работа", 3:"Дети"}
settings = {
    'mode': 0,
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
        json.dump(data, file, indent=2)


def print_menu() -> None:
    """ Главное меню приложения """
    menu_options = {
        1: 'Регистрация',
        2: 'Аутентификация',
        3: 'Просмотр списка пользователей',
        4: 'Просмотр веток форума',
        5: 'Выход'
    }
    for key, value in menu_options.items():
        print(f'{key} ---- {value}')


def check_login(login: str) -> tuple[bool, str]:
    """ Проверка логина пользователя """
    if len(login) < 3 or not login.isalnum() or login.isdigit() or not login[0].isalpha():
        return False, 'Логин введен некорректно. Повторите ввод.'
    user, err = get_user_by_login(login)
    if not err and user:
        return False, 'Имя пользователя уже занято. Повторите ввод.'
    else:
        return True, ''


def check_password(password):
    """ функция для проверки надежности пароля """
    #list_check = [0, 0, 0, 0]
    flag = False
    if len(password) < 6:
        return flag
    else:
        for symbol in password:
            for ranges in [string.ascii_uppercase, string.ascii_lowercase, string.digits]:
                flag = flag or (symbol in ranges)
    return flag



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

    hash_password = hashlib.md5(password.encode()).hexdigest()
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

def authentication():
    pass

def authorization():
    pass

def listing_branch():
    pass

def listing_themes():
    pass

def create_branch():
    pass

def create_themes():
    pass

def create_forum_messages():
    pass

def create_personal_messages():
    pass

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


def print_branches():
    pass

def hacker():
    pass

def finish_program():
    pass


def choose_action():
    """ Функция контроллер приложения. Пользователь выбирает параметр по которому происходит роутинг """
    actions = {
        1: register,
        2: authentication,
        3: print_users,
        4: print_branches,
        5: finish_program,
    }
    select = input("Выберите пункт меню: ")
    result = int(select) if select.isdigit() and 0 < int(select) < 6 else 5
    settings['mode'] = result
    actions[result]()


print_menu()
choose_action()
