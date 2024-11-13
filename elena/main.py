from random import randrange


attempt = 6
letters_remains = [chr(x) for x in range(1040, 1072)]
words = None
number_levels = ["Пять букв", "Шесть букв", "Семь букв", "Восемь букв"]
five_letters = ["АРМИЯ", "АКУЛА", "БАШНЯ", "ВАФЛЯ", "ГАЗОН", "ГУАШЬ"]
six_letters = ["ЙОГУРТ", "ЛИСТЬЯ", "ЧЕРВЯК", "ЯБЛОКО", "БИОЛОГ", "БИЗНЕС", "ГВОЗДЬ"]
seven_letters = ["ЗЕРКАЛО", "ДЖЕКПОТ", "ЛЕОПАРД", "ПОДЪЕЗД", "ДЕЛЬФИН"]
eight_letters = ["ПРОСТУДА", "ДЕТЕКТИВ", "АГЕНСТВО", "ФУТБОЛКА"]
list_letters = [five_letters, six_letters, seven_letters, eight_letters]
dict_letters = {i+1:letter for i, letter in enumerate(list_letters)}

def gallows(attempt):
    if attempt == 0:
        print("_______\n|     |\n|     0\n|    \\|/\n|     |\n|    / \\\n|")
    elif attempt == 1:
        print("_______\n|     |\n|     0\n|    \\|/\n|     |\n|    /\n|")
    elif attempt == 2:
        print("_______\n|     |\n|     0\n|    \\|/\n|     |\n|\n|")
    elif attempt == 3:
        print("_______\n|     |\n|     0\n|    \\| \n|     |\n|\n|")
    elif attempt == 4:
        print("_______\n|     |\n|     0\n|     |\n|     |\n|\n|")
    elif attempt == 5:
        print("_______\n|     |\n|     0\n|\n|\n|\n|")
    elif attempt == 6:
        print("_______\n|     |\n|\n|\n|\n|\n|")

def level_selection():
    for index, value in enumerate(number_levels):
        print(f"{index+1}. {value}")
    while True:
        lvl = input(f"Выберите уровень от 1 до {len(number_levels)}: ")
        if lvl.isdigit() and 0<int(lvl)<=len(number_levels):
            return game_levels(lvl)
        else:
            print(f"Введите цифру от 1 до {len(number_levels)}")

def game_levels(lvl):
    global words
    index = randrange(0, len(dict_letters[int(lvl)]))
    words = dict_letters[int(lvl)][index]
    game(words)

def letters_remain():
    global letters_remains
    for i in letters_remains:
        print(i, end=" ")

def found_letter(letters, text, list_words):
    global attempt
    global letters_remains
    print(f"Вы угадали букву!")
    letters_remains.remove(letters.upper())
    while letters.upper() in text:
        list_words[text.index(letters)] = letters
        text[text.index(letters)] = None
    if "_" not in list_words:
        print(f"Вы выиграли! Было загадано слово: {words}")
        exit_game = input('Нажмите "Пробел" для выхода или "Enter" для еще одной игры: ')
        if exit_game == " ":
            print("Пока")
            return
        elif exit_game == "":
            attempt = 6
            letters_remains = [chr(x) for x in range(1040, 1072)]
            level_selection()

def check_letter(text, list_words):
    global attempt
    global letters_remains
    while attempt>0 and "_" in list_words:
        gallows(attempt)
        print(list_words)
        letters_remain()
        letters = input(f"\nВведите букву, у Вас осталось {attempt} попыток:").upper()

        if letters.upper() in letters_remains and letters.upper() in text:
            found_letter(letters, text, list_words)
        elif letters.upper() in letters_remains and letters.upper() not in text:
            print(f"Вы не угадали букву!")
            letters_remains.remove(letters.upper())
            attempt-=1
        else:
            print(f"Введите букву из списка")

        if attempt<=0:
            gallows(attempt)
            print()
            print(f'Вы проиграли. Было загадано слово: "{words}"')
            exit_game=input('Нажмите "Пробел" для выхода или "Enter" для еще одной игры: ')
            if exit_game==" ":
                print("Пока")
                return
            elif exit_game=="":
                attempt = 6
                letters_remains = [chr(x) for x in range(1040, 1072)]
                level_selection()

def game(words):
    text = list(words)
    list_words = ["_" for _ in range(len(words))]
    check_letter(text, list_words)

if __name__ == "__main__":
    level_selection()


