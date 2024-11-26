import re

def check_password(password):
    """ функция для проверки надежности пароля """
    return re.search("(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])^[a-zA-Z0-9]{6,}$", password)