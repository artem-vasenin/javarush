from .get_pers_msgs import get_pers_msgs
from .print_pers_msgs import print_pers_msgs

def show_new_pers_messages(login: str):
    """ Функция печатающая новые личные сообщения пользователя """
    data, err = get_pers_msgs(login)
    print_pers_msgs(list(filter(lambda x: not x['was_read'], data[login])) if not err else [], err)