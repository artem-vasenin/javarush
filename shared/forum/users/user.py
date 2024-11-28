import re
import json
import hashlib
import os.path
from datetime import datetime

import shared.forum.utils.utils as ut



class Guest:
    def __init__(self):
        pass

    def register(self):
        from shared.forum.main import beginning
        """ Функция регистрации нового пользователя """
        role = 'user'
        login = input("Введите Ваш логин (только латинские буквы в нижнем регистре и цифры): ").strip()
        check, err = check_login(login)
        if not check:
            print(err)
            guest.register()
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
        if role == 'admin':
            beginning.list_guest = Admin()
        else:
            beginning.list_guest = User()
        print(beginning.list_guest)


    def register_controller(self):
        """ Вызов функции регистрации пользователя """
        from shared.forum.main import beginning
        beginning.list_guest.register()
        beginning.print_menu(guest)
        beginning.choose_action(guest)

    def authentication(self) -> None:
        from shared.forum.main import beginning
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
                print('Неверное имя пользователя или пароль') # Текст ошибки должен быть идентичен
        if data['role']=='admin':
            beginning.list_guest = Admin(login)
        else:beginning.list_guest = User(login)


    def authentication_controller(self):
        """ Вызов функции входа в приложение """
        global guest
        from shared.forum.main import beginning
        beginning.list_guest.authentication()
        print(beginning.list_guest)
        beginning.print_menu()
        beginning.choose_action()


class User(Guest):
    def __init__(self, name):
        self.name = name
        condition = {}

class Admin(User):
    def __init__(self, name):
        self.name = name
        condition = {}


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


@ut.print_list_decorator()
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


def bot():
    pass

def block_users():
    pass

def unblock_users():
    pass

def delete_users():
    pass

def hacker():
    pass
