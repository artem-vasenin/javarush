import users.user as user
import branches.forum as forum
import messages.message as messages
import shared.forum.app.state as state

class Beginning:
    def __init__(self):
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

    def print_menu(self, user):
        if type(user)==Guest:
            for key, value in self.menu_guest.items():
                print(f'{key} ---- {value}')
        elif type(user)==User:
            for key, value in self.menu_user.items():
                print(f'{key} ---- {value}')
        elif type(user)==Admin:
            for key, value in self.menu_admin.items():
                print(f'{key} ---- {value}')

    def choose_action(self, user):
        """ Функция контроллер приложения. Пользователь выбирает параметр по которому происходит роутинг """
        if type(user) == Guest:
            actions = {
                1: register_controller,
                2: authentication_controller,
                3: listing_branch_controller,
                4: finish_program
            }
        elif type(user) == User:
            actions = {
                1: print_users_controller,
                2: listing_branch_controller,
                3: personal_messages_controller,
                4: personal_account,
                5: finish_program
            }
        elif type(user) == Admin:
            actions = {
                1: print_users_controller,
                2: listing_branch_controller,
                3: personal_messages_controller,
                4: personal_account,
                5: personal_account_admin,
                6: finish_program
            }
        while True:
            try:
                select = input("Выберите пункт меню: ")
                result = int(select)
                actions[result]()
            except KeyError:
                print(f"Введите число от 1 до {len(actions)}")
                beginning.print_menu(user)
            except ValueError:
                print(f"Введите натуральное число от 1 до {len(actions)}")
                beginning.print_menu(user)



class Guest:
    def __init__(self):
        condition = {}

    def register(self):
        pass

def personal_account():
    pass

def personal_account_admin():
    pass

# def print_menu() -> None:
#     """ Главное меню приложения """
#     usr = state.state.get_user()
#     menu_options = {
#         1: 'Просмотр списка пользователей',
#         2: 'Просмотр веток форума',
#         3: 'Личные сообщения',
#         4: 'Выход'
#     } if usr else {
#         1: 'Регистрация',
#         2: 'Аутентификация',
#         3: 'Просмотр веток форума',
#         4: 'Завершить программу'
#     }
#     for key, value in menu_options.items():
#         print(f'{key} ---- {value}')
#
#     if usr:
#         msgs, err = messages.get_pers_msgs(usr['login'])
#         if not err:
#             not_read = list(filter(lambda x: not x['was_read'], msgs[usr['login']]))
#             print(f'У вас новых сообщений {len(not_read)}. Всего {len(msgs[usr['login']])}.')


def return_to_main_menu():
    """ Функция возвращающая главное меню и выбор его пункта """
    print_menu()
    choose_action()


def authentication_controller():
    """ Вызов функции входа в приложение """
    user.authentication()
    print_menu()
    choose_action()


def register_controller():
    """ Вызов функции регистрации пользователя """
    user.register()
    print_menu()
    choose_action()


def print_users_controller():
    """ Функция контроллер для показа списка пользователей """
    user.print_users()


def listing_branch_controller():
    """ Функция контроллер для меню веток форума """
    count = forum.print_branch()
    select = input("Выберите пункт меню: ")
    forum.check_menu_branch(select, count)


def personal_messages_controller():
    """ Функция контроллер вызова меню личных сообщений """
    messages.personal_messages(return_to_main_menu)

def finish_program():
    """ Функция завершения раюоты приложения """
    return

def logout():
    """ Функция очищающая сессию пользователя после выхода. """
    state.state.logout()
    return_to_main_menu()



# def choose_action():
#     """ Функция контроллер приложения. Пользователь выбирает параметр по которому происходит роутинг """
#     usr = state.state.get_user()
#     actions = {
#         1: print_users_controller,
#         2: listing_branch_controller,
#         3: personal_messages_controller,
#         4: logout,
#     } if usr else {
#         1: register_controller,
#         2: authentication_controller,
#         3: listing_branch_controller,
#         4: finish_program,
#     }
#
#     select = input("Выберите пункт меню: ")
#     result = int(select) if select.isdigit() and 0 < int(select) <= len(actions) else len(actions)
#     actions[result]()



# if __name__ == "__main__":
#     return_to_main_menu()

guest = Guest()
beginning = Beginning()
beginning.print_menu(guest)
beginning.choose_action(guest)
