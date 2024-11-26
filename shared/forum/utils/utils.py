def print_list_decorator(length=60, symbol='='):
    """ Декоратор для печати списков. Должен оборачивать функции возвращающие список строк из 1 и более элементов """
    def decorator(func):
        def wrapper(*args, **kwargs):
            lst = func(*args, **kwargs)
            print(symbol * length)
            for i in range(len(lst)):
                print(lst[i])
                print('-' * length) if not i + 1 == len(lst) else None
            print(symbol * length)
        return wrapper
    return decorator