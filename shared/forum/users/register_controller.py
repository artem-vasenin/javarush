from .check_login import check_login
from .check_password import check_password
from .crypt_password import crypt_password
from .save_user_to_db import save_user_to_db
from datetime import datetime


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