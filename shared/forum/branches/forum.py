import os
import json

from shared.forum.utils.utils import print_list_decorator as print_d

class Branch:
    def __init__(self):
        self.branches = {}
        self.branc = None
        self.tema = None

    def get_branches_from_db(self) -> tuple[dict, str]:
        from shared.forum.main import branch
        """ Функция получающая содержание текущей ветки. При успехе возвращает словарь
        при неудаче возвращает пустой словарь и ошибку"""
        users_db = [f for f in os.listdir(os.path.join(os.getcwd(), 'branches', branch.branc, )) if '.json' in f]
        data = {}

        if not len(users_db):
            return data, 'База данных не найдена'

        with open(os.path.join(os.getcwd(), 'branches', branch.branc, 'themes.json'), encoding="utf-8") as file:
            data = json.load(file)

        return (data, '') if data["branch_name"]["themes"] else (data, 'Список тем пуст')


def print_branch():
    from shared.forum.main import branch
    from shared.forum.main import beginning
    """ Функция печатающая меню бранчей """
    from shared.forum.users.user import Admin
    count = 1
    contents = os.listdir(os.path.join(os.getcwd(), 'branches'))
    try:
        for i in range(len(contents)):
            if os.path.isdir(os.path.join(os.getcwd(), 'branches', contents[i])):
                with open(os.path.join(os.getcwd(), 'branches', contents[i], 'themes.json'),
                          encoding="utf-8") as file:
                    data = json.load(file)
                branch.branches[count] = contents[i]
                print(f"{count}. {data["branch_name"]["title"]}")
                count += 1
    except FileNotFoundError:
        print("", end="")
    print("__________________________")
    print(f"{count}. Назад")
    if type(beginning.list_guest) == Admin:
        print("__________________________")
        print(f"{count + 1}. Добавить новую ветку\n{count + 2}. Удалить действующую ветку")
    return count


def check_menu_branch(select, count):
    from shared.forum.main import beginning, branch
    from shared.forum.users.user import Admin
    """ функция проверки введенных данный в меню branch  """

    while True:
        if type(beginning.list_guest) == Admin and select.isdigit() and int(select)==count+1:
            create_branch()
            break
        elif type(beginning.list_guest) == Admin and select.isdigit() and int(select)==count+2:
            delete_branches()
            break
        elif branch.branches and select.isdigit() and 0<int(select)<count:
            branch.branc = branch.branches[int(select)]
            listing_themes()
            break

        elif select.isdigit() and int(select)==count:
            from shared.forum.main import beginning
            print(beginning.list_guest)
            beginning.return_to_main_menu()
            return

        else:
            select = input("Выберите корректный пункт меню: ")

def listing_branch_controller():
    """ Функция контроллер для меню веток форума """

    count = print_branch()
    select = input("Выберите пункт меню: ")
    check_menu_branch(select, count)
    listing_themes_controller()


@print_d()
def listing_themes():
    from shared.forum.main import branch
    """ функция печатающая список тем в выбранной ветки """
    data, err = branch.get_branches_from_db()
    print(f"\nТемы ветки '{data["branch_name"]["title"]}': ")

    if err:
        return [err]
    else:
        themes = data["branch_name"]["themes"]
        return [f"{i+1}. {themes[i]["title_themes"]}" for i in range(len(themes))]+[f"{len(data)+2}. Назад"]


def create_branch():
    print("Добавляю ветку")


def create_themes():
    pass


def delete_branches():
    print("Удаляю ветку")


def create_forum_messages():
    pass

def print_themes(select):
    pass

def listing_themes_controller():
    """ Функция контроллер для меню веток форума """
    listing_themes()
    select = input("Выберите пункт меню: ")
    print_themes(select)