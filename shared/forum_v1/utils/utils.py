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


def translit(text):
    ru = {'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ж': 'ZH', 'З': 'Z', 'И': 'I', 'Й': 'J',
          'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F',
          'Х': 'KH', 'Ц': 'C', 'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SHH', 'Ъ': '``', 'Ы': 'Y', 'Ь': '`', 'Э': 'E`', 'Ю': 'YU',
          'Я': 'YA',
          'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'j',
          'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f',
          'х': 'kh', 'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'shh', 'ъ': '``', 'ы': 'y', 'ь': '`', 'э': 'e`', 'ю': 'yu',
          'я': 'ya'
          }
    texts = ""
    for i in range(len(text)):
        if text[i] in ru:
            x = ru[text[i]]
            texts += x
        else:
            texts += text[i]
    return texts