import random
def generate_list_of_digits():
    """
    Функция генерирует список из цифр
    """
    digits_list = []
    for i in range(10):
        digits_list.append(i)
    return digits_list

def generate_list_of_lowercase_english_letters():
    """
    Функция генерирует список из английских букв в нижнем регистре
    """
    lowercase_english_letters_list = []
    for ascii_code in range(97, 123):
        lowercase_english_letters_list.append(chr(ascii_code))
    return lowercase_english_letters_list

def generate_list_of_uppercase_english_letters():
    """
    Функция генерирует список из английских букв в верхнем регистре
    """
    uppercase_english_letters_list = []
    for ascii_code in range(65, 91):
        uppercase_english_letters_list.append(chr(ascii_code))
    return uppercase_english_letters_list

def generate_list_of_special_symbols():
    """
    Функция генерирует список из спецсимволов
    """
    special_symbols_list_ascii = list(range(33, 48)) + list(range(58, 65)) + list(range(91, 97)) + list(range(123, 127))
    special_symbols_list = []
    for ascii_code in special_symbols_list_ascii:
        special_symbols_list.append(chr(ascii_code))
    return special_symbols_list

def input_password_length():
    count = 0
    flag = True
    while flag:
        password_length = input("Выберите длину желаемого пароля, но не больше 500: ")
        if password_length.isdigit():
            flag = False #Пользователь ввел цифру
            password_length = int(password_length)
            if password_length > 1000:
                print(f'Запрашиваемая длина пароля {password_length}, что больше 1000, вы хотите повесить сервер? Повторите ввод')
                flag = True
            elif password_length > 500:
                print(f'{password_length} > 500')
                flag = True
        else:
            count += 1
            if count <= 1:
                print(f'{password_length} это не цифра, повторите ввод')
            elif count <=5:
                print(f'Вы очень упорны, но {password_length} не является цифрой')
            elif count > 10:
                print(f'Хватит мучать программу')
    return password_length



def choose_dicts():
    """
    Данная функция составляет итоговый список
    Хочу разбить её на 2, т.к. много повторений но пока так
    """
    flag = True
    result_list = []
    while flag:
        print("Выберите словари для генерации пароля")
        need_all = input("Введите ALL, если в пароле потребуются все имеющиеся словари: ").upper()
        if need_all == "ALL":
            result_list.extend(generate_list_of_digits())
            result_list.extend(generate_list_of_lowercase_english_letters())
            result_list.extend(generate_list_of_uppercase_english_letters())
            result_list.extend(generate_list_of_special_symbols())
        else:
            need_digits = input("Введите YES, если в пароле потребуются цифры: ").upper()
            if need_digits == 'YES':
                result_list.extend(generate_list_of_digits())
            need_lowercase = input("Введите YES, если в пароле потребуются английские буквы в нижнем регистре: ").upper()
            if need_lowercase == 'YES':
                result_list.extend(generate_list_of_lowercase_english_letters())
            need_uppercase = input("Введите YES, если в пароле потребуются английские буквы в верхнем регистре: ").upper()
            if need_uppercase == 'YES':
                result_list.extend(generate_list_of_uppercase_english_letters())
            need_special_symbols = input("Введите YES, если в пароле потребуются специальные символы: ").upper()
            if need_special_symbols == 'YES':
                result_list.extend(generate_list_of_special_symbols())

        if len(result_list) == 0:
            print('Вы не выбрали ни одного словаря, повторите выбор')
        else:
            return result_list
            flag = False

def generate_password(password_list, password_length):
    """
    Данная функция генерирует пароль
    """
    password = ''
    for _ in range(password_length):
        password += str(random.choice(password_list))
    return password

generate_list_of_digits()
generate_list_of_lowercase_english_letters()
generate_list_of_uppercase_english_letters()
generate_list_of_special_symbols()
password_length = input_password_length()
password_list = choose_dicts()
print(f'Ваш пароль :{generate_password(password_list, password_length)}')






