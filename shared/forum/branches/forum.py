import os
import json

import shared.forum.app.status as status
from shared.forum.utils.utils import print_list_decorator as print_d


def get_branches_from_db() -> tuple[dict, str]:
    """ Функция получающая содержание текущей ветки. При успехе возвращает словарь
    при неудаче возвращает пустой словарь и ошибку"""
    users_db = [f for f in os.listdir(os.path.join(os.getcwd(), 'branches', status.statu.stat["branch"][0], )) if '.json' in f]
    data = {}

    if not len(users_db):
        return data, 'База данных не найдена'

    with open(os.path.join(os.getcwd(), 'branches', status.statu.stat["branch"][0], 'themes.json'), encoding="utf-8") as file:
        data = json.load(file)

    return (data, '') if data["branch_name"]["themes"] else (data, 'Список тем пуст')


def print_branch():
    """ Функция печатающая меню бранчей """
    """ Функция печатающая меню бранчей """
    count = 1
    contents = os.listdir(os.path.join(os.getcwd(), 'branches'))
    try:
        for i in range(len(contents)):
            if os.path.isdir(os.path.join(os.getcwd(), 'branches', contents[i])):
                with open(os.path.join(os.getcwd(), 'branches', contents[i], 'themes.json'), encoding="utf-8") as file:
                    data = json.load(file)
                status.statu.status_branch(contents[i], count)
                print(f"{count}. {data["branch_name"]["title"]}")
                count += 1
    except FileNotFoundError:
        print("", end="")
    print("__________________________")
    print(f"{count}. Назад")
    if status.statu.stat['user'] and status.statu.stat['user']["role"] == "admin":
        print("__________________________")
        print(f"{count + 1}. Добавить новую ветку\n{count + 2}. Удалить действующую ветку")
    return count


def check_menu_branch(select, count):
    """ функция проверки введенных данный в меню branch  """
    # st = app.get_state()
    is_admin = status.statu.stat["user"] and status.statu.stat["user"]["role"] == "admin"

    while True:
        if is_admin and select.isdigit() and int(select)==count+1:
            create_branch()
            break
        elif is_admin and select.isdigit() and int(select)==count+2:
            delete_branches()
            break
        elif status.statu.stat["branch"] and select.isdigit() and 0<int(select)<count:
            branch = status.statu.stat["branch"][int(select)]
            status.statu.status_branch(branch, 0)

            if status.statu.stat["branch"][int(select)-1]:
                theme = status.statu.stat["branch"][int(select)-1]
                status.statu.status_branch(theme, 0)
                print( status.statu.stat["branch"])
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