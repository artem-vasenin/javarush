import os
import json

import shared.forum.app.state as state
from shared.forum.utils.utils import print_list_decorator as print_d


def get_branches_from_db() -> tuple[dict, str]:
    """ Функция получающая содержание текущей ветки. При успехе возвращает словарь
    при неудаче возвращает пустой словарь и ошибку"""
    brnh = state.state.get_branch()
    users_db = [f for f in os.listdir(os.path.join(os.getcwd(), 'branches', brnh[0], )) if '.json' in f]
    data = {}

    if not len(users_db):
        return data, 'База данных не найдена'

    with open(os.path.join(os.getcwd(), 'branches', brnh[0], 'themes.json'), encoding="utf-8") as file:
        data = json.load(file)

    return (data, '') if data["branch_name"]["themes"] else (data, 'Список тем пуст')


def print_branch():
    """ Функция печатающая меню бранчей """
    """ Функция печатающая меню бранчей """
    count = 1
    contents = os.listdir(os.path.join(os.getcwd(), 'branches'))
    usr = state.state.get_user()
    try:
        for i in range(len(contents)):
            if os.path.isdir(os.path.join(os.getcwd(), 'branches', contents[i])):
                with open(os.path.join(os.getcwd(), 'branches', contents[i], 'themes.json'), encoding="utf-8") as file:
                    data = json.load(file)
                state.state.set_branch(contents[i], count)
                print(f"{count}. {data["branch_name"]["title"]}")
                count += 1
    except FileNotFoundError:
        print("", end="")
    print("__________________________")
    print(f"{count}. Назад")
    if usr and usr["role"] == "admin":
        print("__________________________")
        print(f"{count + 1}. Добавить новую ветку\n{count + 2}. Удалить действующую ветку")
    return count


def check_menu_branch(select, count):
    """ функция проверки введенных данный в меню branch  """
    usr = state.state.get_user()
    brnh = state.state.get_branch()
    is_admin = usr and usr["role"] == "admin"

    while True:
        if is_admin and select.isdigit() and int(select)==count+1:
            create_branch()
            break
        elif is_admin and select.isdigit() and int(select)==count+2:
            delete_branches()
            break
        elif brnh and select.isdigit() and 0<int(select)<count:
            branch = brnh[int(select)]
            state.state.set_branch(branch, 0)

            if brnh[int(select)-1]:
                theme = brnh[int(select)-1]
                state.state.set_branch(theme, 0)
                print( brnh)
                listing_themes()
            else:
                print('Ошибка получения темы')
            break
        elif select.isdigit() and int(select)==count:
            # надо подумать как вызывать главное меню. Наверное меню тоже надо в модуль вынести
            # return_to_main_menu()
            break
        else:
            select = input("Выберите корректный пункт меню: ")


@print_d()
def listing_themes():
    """ функция печатающая список тем в выбранной ветки """
    data, err = get_branches_from_db()
    print(f"\nТемы ветки '{data["branch_name"]["title"]}': ")

    if err:
        return [err]
    else:
        themes = data["branch_name"]["themes"]
        return [f"{i+1}. {themes[i]["title_themes"]}" for i in range(len(themes))]



def create_branch():
    print("Добавляю ветку")


def create_themes():
    pass


def delete_branches():
    print("Удаляю ветку")


def create_forum_messages():
    pass