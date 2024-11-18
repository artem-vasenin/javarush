import hashlib
from datetime import datetime
import json
import os.path
import string

dict_branch = {1: {"Погода":["Опять дождь", "Невыносимая жара", "Мороз"]}, 2:"Работа", 3:"Дети"}
settings = {
    'mode': 0,
    'role': None,
}

def write_post():
    pass

def print_menu() -> None:
    """ Функция стартер приложения """
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
    elif os.path.exists(os.path.join(os.getcwd(), "users", login+".csv")):
        return False, 'Имя пользователя уже занято. Повторите ввод.'
    else:
        return True, ''

def check_password(password):
    # функция для проверки надежности пароля
    list_check = [0, 0, 0, 0]
    for i in password:
        if i in string.ascii_uppercase:
            list_check[0] +=1
        if i in string.ascii_lowercase:
            list_check[1] +=1
        if i in string.digits:
            list_check[2] +=1
        if len(password) > 5:
            list_check[3] +=1
    return not list_check.count(0)

def register():
    global admin
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
    """ 
    по запросу секретного ключа, если он не верный (не найден среди действующих), может запрашивать у пользователя: 
    "Вы хотите зарегистрироваться как обычный пользователь или админ?" если админ, то просит ввести ключ повторно
     """
    secretkey = input("Введите секретный ключ (для привилегированных пользователей): ")
    if secretkey != "тут будет очень секретный ключ":
        admin = True

    with open(os.path.join(os.getcwd(), "users", login+".json"), 'w', encoding="utf-8") as file:
        user = {
            'login': login,
            'passhash': hash_password,
            'role': 'admin' if admin else 'user',
            'blocked_at': '',
            'blocked_reason': '',
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'name': '',
            'city': '',
        }
        json.dump(user, file, indent=2)

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

def get_user_list() -> list:
    users_files = [f for f in os.listdir(os.path.join(os.getcwd(), "users")) if '.json' in f]
    users = []
    for user_file in users_files:
        with open(os.path.join(os.getcwd(), "users", user_file), encoding="utf-8") as file:
            users.append(json.load(file))
    return users

def print_users() -> None:
    users = get_user_list()
    print('='*60)
    if not len(users):
        print('Список пользователей пока пуст...')
    else:
        for i in range(len(users)):
            print(f'login: {users[i]["login"]} | role: {users[i]["role"]} | registered: {users[i]["created_at"]}')
            print('-'*60 if i + 1 < len(users) else '', end='\n' if i + 1 < len(users) else '')
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
