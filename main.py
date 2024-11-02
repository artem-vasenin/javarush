from random import randrange
attempt = 6
letters_remains = ["а", "б", "в", "г", "д", "е", "ж", "з", "и", "й", "к", "л", "м", "н", "о", "п", "р", "с" , "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ь", "ы", "ъ", "э", "ю", "я"]
slovo = None
number_levels = ["Пять букв", "Шесть букв", "Семь букв", "Восемь букв"]
five_letters = ["армия", "акула", "башня", "вафля", "газон", "гуашь"]
six_letters = ["йогурт", "лстья", "червяк", "яблоко", "биолог", "бизнес", "гвоздь"]
seven_letters = ["зеркало", "джекпот", "леопард", "подъезд", "дельфин"]
eight_letters = ["авимбуве", "детектив", "агенство"]
def level_selection():
    for index, value in enumerate(number_levels):
        print(f"{index+1}. {value}")
    while True:
        lvl = input(f"Выбирите уровень от 1 до {len(number_levels)}: ")
        if lvl.isdigit() and 0 < int(lvl) <= len(number_levels):
            return game_levels(lvl)
        else:
            print(f"Введите цифру от 1 до {len(number_levels)}")
def game_levels(lvl):
    if int(lvl) == 1:
        levels_one()
    elif int(lvl) == 2:
        levels_two()
    elif int(lvl) == 3:
        levels_three()
    elif int(lvl) == 4:
        levels_four()
def levels_one():
    global slovo
    index = randrange(1, len(five_letters))
    slovo = five_letters[index]
    game(slovo)

def levels_two():
    global slovo
    index = randrange(1, len(six_letters))
    slovo = six_letters[index]
    game(slovo)

def levels_three():
    global slovo
    index = randrange(1, len(seven_letters))
    slovo = seven_letters[index]
    return game(slovo)

def levels_four():
    global slovo
    index = randrange(1, len(eight_letters))
    slovo = eight_letters[index]
    game(slovo)


def letters_remain():
    global letters_remains
    for i in letters_remains:
        print(i, end=" ")

def slov(slovo):
    print("Ваше слово:", "*"*len(slovo))


def game(slovo):
    global attempt
    text = list(slovo)
    list_slovo = ["*" for i in range(len(slovo))]
    while attempt>0:

        print(list_slovo)
        letters_remain()
        letters = input(f"\nВведите букву, у Вас оталось {attempt} попыток:")
        if letters.lower() in letters_remains and letters.lower() in text:
            print(f"Вы угадали букву!")
            letters_remains.remove(letters.lower())
            while letters.lower() in text:
                list_slovo[text.index(letters)] = letters
                text[text.index(letters)] = None
            if "*" not in list_slovo:
                print(f"Вы выиграли! Было загадано слово: {slovo}")
                exit = input("Нажмите Enter для выхода: ")
                if exit == "":
                    "Пока"
                    return
        elif letters.lower() in letters_remains and letters.lower() not in text:
            print(f"Вы не угадали букву!")
            letters_remains.remove(letters.lower())
            attempt -= 1
        else:
            print(f"Введити букву из списка")
        if attempt<=0:
            print(f'Вы проиграли. Было загаданно слово: "{slovo}"')
            exit = input("Нажмите Enter для выхода: ")
            if exit == "":
                "Пока"




if __name__ == "__main__":
    level_selection()


