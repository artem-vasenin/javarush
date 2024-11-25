import hashlib
from datetime import datetime
import json
import os.path
import re

from shared.forum.messages.get_pers_msgs import get_pers_msgs
from shared.forum.messages.personal_messages_controller import personal_messages_controller
from shared.forum.users import get_user_by_login, save_user_to_db, print_users

# Состояние приложения. Пишем сюда данные авторизованного пользователя и всякие флаги
state = {
    'branch': {},
    'route': 0,
    'user': {},
}

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
    """ функция печатающая список тем в выбранной ветки """
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

def bot():
    pass

def block_users():
    pass

def unblock_users():
    pass

def delete_users():
    pass

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
    def get_pers_msgs_controller():
        personal_messages_controller(state['user']['login'], return_to_main_menu)

    actions = {
        1: print_users,
        2: listing_branch_controller,
        3: get_pers_msgs_controller,
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
