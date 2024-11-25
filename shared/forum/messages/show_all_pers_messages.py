from .get_pers_msgs import get_pers_msgs
from .print_pers_msgs import print_pers_msgs

def show_all_pers_messages(login: str):
    """ Функция печатающая все личные сообщения пользователя """
    data, err = get_pers_msgs(login)
    print_pers_msgs(data[login] if not err else [], err)