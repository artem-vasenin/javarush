from shared.forum.messages.show_all_pers_messages import show_all_pers_messages
from shared.forum.messages.show_new_pers_messages import show_new_pers_messages
from shared.forum.messages.send_personal_message import send_personal_message

def personal_messages_controller(login: str, cb):
    """ Функция-контроллер для функционала личных сообщений """
    actions = {
        1: {'title': 'Показать все сообщения', 'action': show_all_pers_messages},
        2: {'title': 'Показать непрочитанные сообщения', 'action': show_new_pers_messages},
        3: {'title': 'Написать личное сообщение', 'action': send_personal_message},
        4: {'title': 'Выйти в главное меню', 'action': None},
    }
    print(*[f'{k}: {v['title']}' for k, v in actions.items()], sep='\n')

    def check(val: str) -> bool:
        return val.isdigit() and 0 < int(val) < 5

    res = input('Сообщения. Выберите пункт меню: ')
    while not check(res):
        res = input('Сообщения. Выберите пункт меню. Опять...: ')

    if int(res) == 4:
        cb()
    else:
        actions[int(res)]['action'](login)