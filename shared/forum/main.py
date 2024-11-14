import hashlib
import datetime
import os.path

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
    return user_choose

def choose_action():
    user_choose = print_menu()
    if user_choose == 1:
        register()
    elif user_choose == 2:
        authentication()
    elif user_choose == 3:
        get_user_lists()
    elif user_choose == 4:
        print_branches()
    elif user_choose == 5:
        return None

def register():
    """
    Простая регистрация без проверки сложности пароля (пока)
    """
    login = input("Введите Ваше имя пользователя: ")
    password = input("Введите Ваш пароль")
    secretkey = input("Введите секретный ключ (для привилегированных пользователей): ")
    hash = hashlib.md5(password.encode()).hexdigest()
    if login != '' and hash !='':
        if os.path.exists(f'/home/forum/users/{login}'):
            print(f'Имя пользователя {login} уже существует, придумайте другое')
        else:
            with open(f'/home/forum/users/{login}', 'w', encoding="utf-8") as file:
                file.write(login)
                file.write(hash)


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