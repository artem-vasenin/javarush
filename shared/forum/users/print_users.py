from shared.forum.users import get_users_from_db
from shared.forum.utils.print_list_decorator import print_list_decorator


@print_list_decorator()
def print_users() -> list[str]:
    """ Функция запрашивающая список пользователей и выводящая его на печать. Когда будет присвоение ролей надо ее дописать """
    data, err = get_users_from_db()
    if err:
        return [err]
    else:
        lst = []
        for i in range(data['len']):
            u = data['users'][i]
            blocked = f' blocked: {u["blocked_at"]}' if u['blocked_at'] else ''
            lst.append(f'login: {u["login"]} | role: {u["role"]} | registered: {u["created_at"]}{blocked}')

        return lst
