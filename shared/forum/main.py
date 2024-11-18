import hashlib
import datetime
import os.path
from itertools import count
import string

admin = False

def write_post(self):
    pass

def print_menu():
    menu_options = {
        1: 'Регистрация',
        2: 'Аутентификация',
        3: 'Просмотр списка пользователей',
        4: 'Просмотр веток форума',
        5: 'Выход'
    }
    for key, value in menu_options.items():
        print(f'{key} ---- {value}')
    user_choose = input("Выберите пункт меню: ")
    while True:
        if user_choose.isdigit() and 0<int(user_choose)<6:
            choose_action(user_choose)
            break
        else:
            user_choose = input(f"Выберите пункт от 1 до {len(menu_options)}: ")

def choose_action(user_choose):
    if int(user_choose) == 1:
        register()
    elif int(user_choose)  == 2:
        authentication()
    elif int(user_choose)  == 3:
        get_user_lists()
    elif int(user_choose)  == 4:
        print_branches()
    elif int(user_choose)  == 5:
        return None

def check_login(login: str):
    """ Проверка логина пользователя """
    if len(login) < 3 or not login.isalnum() or login.isdigit() or not login[0].isalpha():
        return False, 'Логин введен некорректно. Повторите ввод.'
    elif os.path.exists(f'{os.getcwd()}/users/{login}.txt'):
        return False, 'Имя пользователя уже занято. Повторите ввод.'
    else:
        return True, ''

def check_password(password):
    # функция для проверки надежности пароля
    count = 0
    for i in password:
        if i in string.ascii_uppercase:
            count+=1
            break
    for i in password:
        if i in string.ascii_lowercase:
            count+=1
            break
    for i in password:
        if i in string.digits:
            count+=1
            break
    if len(password)>5:
        count += 1
    if count == 4:
        return True
    else:
        return False

def register():
    global admin
    current_directory = os.getcwd()
    login = input("Введите Ваш логин (только латинские буквы и цифры): ").strip()
    check, err = check_login(login)
    if not check:
        print(err)
        register()
        return

    password = input("Введите Ваш пароль: ")
    while not check_password(password):
        password = input("Пароль не безопасный, введите другой: ")
    hash_password = hashlib.md5(password.encode()).hexdigest()
    with open(f'{current_directory}\\users\\{login}.txt', 'w', encoding="utf-8") as file:
        file.write(login)
        file.write(hash_password)
    """ 
    по запросу секретного ключа, если он не верный (не найден среди действующих), может запрашивать у пользователя: 
    "Вы хотите зарегистрироваться как обычный пользователь или админ?" если админ, то просит ввести ключ повторно
     """
    secretkey = input("Введите секретный ключ (для привилегированных пользователей): ")
    if secretkey!="тут будет очень секретный ключ":
        admin = True

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

def get_user_lists():
    pass

def print_branches():
    pass

def hacker():
    pass


print_menu()