import hashlib
from datetime import datetime
import json
import os.path
import re

login_role_dict = {"login":"Lena", "role":"admin"}
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
        json.dump(data, file, indent=2, ensure_ascii=False)


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
    return flag # ToDo: не забываем о красоте кода, отступах между функциями, условиями и переменными по возможности тоже
def authorization():
    pass


def listing_branch():
    count = 1
    contents = os.listdir(os.path.join(os.getcwd(), 'branches'))
    for i in range(len(contents)):
        if os.path.isdir(os.path.join(os.getcwd(), 'branches', contents[i])):
            print(f"{count}. {contents[i]}")
            count += 1
    if login_role_dict["role"] == "admin":
        print("__________________________")
        print(f"{count}. Добавить новую ветку\n{count + 1}. Удалить действующую ветку")
    select = input("Выберите пункт меню: ")
    check_menu_branch(select, count)


def check_menu_branch(select, count):
    while True:
        if login_role_dict["role"] == "admin" and select.isdigit() and int(select)==count:
            create_branch()
            break
        elif login_role_dict["role"] == "admin" and select.isdigit() and int(select)==count+1:
            delete_branches()
            break
        elif select.isdigit() and 0<int(select)<count:
            listing_themes()
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



def delete_branches():
    print("Удаляю ветку")

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
        4: listing_branch,
        5: finish_program,
    }
    select = input("Выберите пункт меню: ")
    result = int(select) if select.isdigit() and 0 < int(select) < 6 else 6
    while result==6:
        select = input(f"Введите корректно пункт меню, число от 1 до {len(actions)}: ")
        result = int(select) if select.isdigit() and 0 < int(select) < 6 else 6
    settings['mode'] = result
    actions[result]()


print_menu()
choose_action()
