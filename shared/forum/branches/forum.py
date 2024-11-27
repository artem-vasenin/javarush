import os
import json

import shared.forum.app.app as app
from shared.forum.utils.utils import print_list_decorator as print_d


def get_branches_from_db() -> tuple[dict, str]:
    """ Функция получающая содержание текущей ветки. При успехе возвращает словарь
    при неудаче возвращает пустой словарь и ошибку"""
    st = app.get_state()
    users_db = [f for f in os.listdir(os.path.join(os.getcwd(), 'branches', st.get("branch"), )) if '.json' in f]
    data = {}

    if not len(users_db):
        return data, 'База данных не найдена'

    with open(os.path.join(os.getcwd(), 'branches', st.get("branch"), 'themes.json'), encoding="utf-8") as file:
        data = json.load(file)

    return (data, '') if data["branch_name"]["themes"] else (data, 'Список тем пуст')


def print_branch():
    """ Функция печатающая меню бранчей """
    st = app.get_state()
    url = os.path.join(os.getcwd(), 'branches')
    count = 1
    dirs = [entry.name for entry in os.scandir(url) if (entry.is_dir() and entry.name != '__pycache__')]
    dct = {}

    for i in range(len(dirs)):
        print(f"{count}. {dirs[i]}")
        dct[count] = dirs[i]
        count += 1
    app.save_state('branch', dct)

    if st.get('user') and st['user']["role"] == "admin":
        print("_"*40)
        print(f"{count + 1}. Добавить новую ветку\n{count + 2}. Удалить действующую ветку")
    return count


def check_menu_branch(select, count):
    """ функция проверки введенных данный в меню branch  """
    st = app.get_state()
    is_admin = st.get('user') and st['user']["role"] == "admin"

    while True:
        if is_admin and select.isdigit() and int(select)==count+1:
            create_branch()
            break
        elif is_admin and select.isdigit() and int(select)==count+2:
            delete_branches()
            break
        elif st.get('branch') and select.isdigit() and 0<int(select)<count:
            branch = st.get('branch')

            if branch.get(select):
                theme = branch[select]
                app.save_state('branch', theme)
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