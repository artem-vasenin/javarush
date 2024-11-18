import hashlib
from datetime import datetime
import os.path
import string

settings = {
    'mode': None,
    'role': None,
}

# ToDo: хмммм откуда self в процедурном то варианте?)
def write_post(self):
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

def get_user_by_login(login: str) -> str:
    pass

def check_login(login: str):
    """ Проверка логина пользователя """
    if len(login) < 3 or not login.isalnum() or login.isdigit() or not login[0].isalpha():
        return False, 'Логин введен некорректно. Повторите ввод.'
    elif os.path.exists(os.path.join(os.getcwd(), "users", login+".txt")):
        return False, 'Имя пользователя уже занято. Повторите ввод.'
    else:
        return True, ''

def check_password(password):
    """ функция для проверки надежности пароля """
    # ToDo: три похожих цикла с разным условием так и просится на отдельную функцию (пока сам не придумал какую...)
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
    # ToDo: тут можно просто сделать return count == 4 (это приведется к булеву и вернется)
    if count == 4:
        return True
    else:
        return False

def register():
    global admin
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
    with open(os.path.join(os.getcwd(), "users", login+".txt"), 'w', encoding="utf-8") as file:
        file.writelines([f'login|{login}\n', f'password|{hash_password}\n', f'createdAt|{datetime.now()}\n'])
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

def get_user_list():
    pass
    # with open(os.path.join(os.getcwd(), "users", login+".txt"), 'w', encoding="utf-8") as file:
    #     file.writelines([f'login|{login}\n', f'password|{hash_password}\n', f'createdAt|{datetime.now()}\n'])

def print_branches():
    pass

def hacker():
    pass

def finish_program():
    pass

def choose_action():
    """ Функция контроллер приложения. Пользователь выбирает параметр по которому происходит роутинг """
    global mode
    actions = {
        1: register,
        2: authentication,
        3: get_user_list,
        4: print_branches,
        5: finish_program,
    }
    select = input("Выберите пункт меню: ")
    result = int(select) if select.isdigit() and 0 < int(select) < 6 else 5
    mode = result
    actions[result]()


print_menu()
choose_action()
