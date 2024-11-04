from random import randrange


attempt = 6
letters_remains = [chr(x) for x in range(1072, 1104)]
words = None
number_levels = ["Пять букв", "Шесть букв", "Семь букв", "Восемь букв"]
five_letters = ["армия", "акула", "башня", "вафля", "газон", "гуашь"]
six_letters = ["йогурт", "лстья", "червяк", "яблоко", "биолог", "бизнес", "гвоздь"] # опечатка лстья
seven_letters = ["зеркало", "джекпот", "леопард", "подъезд", "дельфин"]
eight_letters = ["авимбуве", "детектив", "агенство"]
list_letters = [five_letters, six_letters, seven_letters, eight_letters]
dict_letters = {i+1:letter for i, letter in enumerate(list_letters)}

def level_selection():
    for index, value in enumerate(number_levels):
        print(f"{index+1}. {value}")
    while True:
        lvl = input(f"Выбирите уровень от 1 до {len(number_levels)}: ")
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
    print(f"Вы угадали букву!")
    letters_remains.remove(letters.lower())
    while letters.lower() in text:
        list_words[text.index(letters)] = letters
        text[text.index(letters)] = None
    if "*" not in list_words:
        print(f"Вы выиграли! Было загадано слово: {words}")
        exit = input("Нажмите Enter для выхода: ")
        if exit=="":
            "Пока"
            return

def check_letter(text, list_words):
    global attempt
    while attempt>0 and "*" in list_words:
        print(list_words)
        letters_remain()
        letters = input(f"\nВведите букву, у Вас оталось {attempt} попыток:")
        # ToDo: отступы между блоками условий и переменными
        if letters.lower() in letters_remains and letters.lower() in text:
            found_letter(letters, text, list_words)
        elif letters.lower() in letters_remains and letters.lower() not in text:
            print(f"Вы не угадали букву!")
            letters_remains.remove(letters.lower())
            attempt-=1
        else:
            print(f"Введити букву из списка")
        if attempt<=0:
            print(f'Вы проиграли. Было загаданно слово: "{words}"')
            exit=input("Нажмите Enter для выхода: ")
            if exit=="":
                # ToDo: тут ты еще наерное хотела "покасик" зкавернуть в print?
                "Пока"
                return

def game(words):
    text = list(words)
    list_words = ["*" for i in range(len(words))]
    check_letter(text, list_words)

if __name__ == "__main__":
    level_selection()


