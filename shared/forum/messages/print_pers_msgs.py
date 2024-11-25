from ..utils import print_list_decorator

@print_list_decorator(length=90)
def print_pers_msgs(lst: list, err) -> list[str]:
    """ Функция оформляющая список сообщений перед выводом """
    if err:
        return [err]
    else:
        if len(lst):
            return [f'Отправитель: {x['from'].ljust(10)} | Дата: {x['created_at']} | "{x['message']}"' for x in lst]
        else:
            return ['Сообщений пока нет']