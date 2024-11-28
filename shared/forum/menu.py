import users.user as us
import messages.message as messages
from shared.forum.users.user import Guest, User, Admin
import os.path
import json
from shared.forum.branches.forum import listing_branch_controller

class Beginning:
    def __init__(self):
        self.list_guest = Guest()
        self.menu_guest = {
            1: 'Регистрация',
            2: 'Аутентификация',
            3: 'Просмотр веток форума',
            4: 'Завершить программу'
        }
        self.menu_user = {
            1: 'Просмотр списка пользователей',
            2: 'Просмотр веток форума',
            3: 'Личные сообщения',
            4: 'Личный кабинет',
            5: 'Выход'
        }
        self.menu_admin = {
            1: 'Просмотр списка пользователей',
            2: 'Просмотр веток форума',
            3: 'Личные сообщения',
            4: 'Личный кабинет',
            5: 'Личный кабинет администратора',
            6: 'Выход'
        }


    def print_menu(self):
        from shared.forum.users.user import User
        from shared.forum.main import beginning
        if type(beginning.list_guest)==Guest:
            for key, value in self.menu_guest.items():
                print(f'{key} ---- {value}')
        elif type(beginning.list_guest)==User:
            for key, value in self.menu_user.items():
                print(f'{key} ---- {value}')
        elif type(beginning.list_guest)==Admin:
            for key, value in self.menu_admin.items():
                print(f'{key} ---- {value}')

    def choose_action(self):
        """ Функция контроллер приложения. Пользователь выбирает параметр по которому происходит роутинг """
        from shared.forum.main import beginning
        if type(beginning.list_guest) == Guest:
            actions = {
                1: beginning.list_guest.register_controller,
                2: beginning.list_guest.authentication_controller,
                3: listing_branch_controller,
                4: finish_program
            }
        elif type(beginning.list_guest) == User:
            actions = {
                1: print_users_controller,
                2: listing_branch_controller,
                3: personal_messages_controller,
                4: personal_account,
                5: finish_program
            }
        elif type(beginning.list_guest) == Admin:
            actions = {
                1: print_users_controller,
                2: listing_branch_controller,
                3: personal_messages_controller,
                4: personal_account,
                5: personal_account_admin,
                6: logout
            }
        while True:
            try:
                select = input("Выберите пункт меню: ")
                result = int(select)
                actions[result]()
                return
            except KeyError:
                print(f"Введите число от 1 до {len(actions)}")
                beginning.print_menu()
            except ValueError:
                print(f"Введите натуральное число от 1 до {len(actions)}")
                beginning.print_menu()

    def return_to_main_menu(self):
        from shared.forum.main import beginning
        """ Функция возвращающая главное меню и выбор его пункта """

        beginning.print_menu()
        beginning.choose_action()

    def save_user_to_db(self, user: dict) -> None:
        """ Функция записи пользователя в базу данных """
        data, error = us.get_users_from_db()

        if error and not data:
            data['users'] = [user]
            data['len'] = 1
        else:
            data['users'].append(user)
            data['len'] = len(data['users'])

        with open(os.path.join(os.getcwd(), "users", "users.json"), 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)


def print_users_controller():
    """ Функция контроллер для показа списка пользователей """
    us.print_users()



def personal_messages_controller():
    from shared.forum.main import beginning
    """ Функция контроллер вызова меню личных сообщений """
    messages.personal_messages(beginning.return_to_main_menu)

def finish_program():
    """ Функция завершения раюоты приложения """
    print("Пока")
    return

def logout():
    from shared.forum.main import beginning
    """ Функция очищающая сессию пользователя после выхода. """
    beginning.list_guest = Guest()
    beginning.return_to_main_menu()

def personal_account():
    pass

def personal_account_admin():
    pass
