import hashlib

def crypt_password(password) -> str:
    """ Функция возвращает hash пароля """
    return hashlib.md5(password.encode()).hexdigest()