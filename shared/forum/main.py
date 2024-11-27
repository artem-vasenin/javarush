import users.user as user
import branches.forum as forum
import messages.message as messages
import shared.forum.app.state as state


def print_menu() -> None:
    """ Главное меню приложения """
    usr = state.state.get_user()
    menu_options = {
        1: 'Просмотр списка пользователей',
        2: 'Просмотр веток форума',
        3: 'Личные сообщения',
        4: 'Выход'
    } if usr else {
        1: 'Регистрация',
        2: 'Аутентификация',
        3: 'Просмотр веток форума',
        4: 'Завершить программу'
    }
    for key, value in menu_options.items():
        print(f'{key} ---- {value}')

    if usr:
        msgs, err = messages.get_pers_msgs(usr['login'])
        if not err:
            not_read = list(filter(lambda x: not x['was_read'], msgs[usr['login']]))
            print(f'У вас новых сообщений {len(not_read)}. Всего {len(msgs[usr['login']])}.')


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
    pass

def logout():
    """ Функция очищающая сессию пользователя после выхода. """
    pass


def choose_action():
    """ Функция контроллер приложения. Пользователь выбирает параметр по которому происходит роутинг """
    usr = state.state.get_user()
    actions = {
        1: print_users_controller,
        2: listing_branch_controller,
        3: personal_messages_controller,
        4: logout,
    } if usr else {
        1: register_controller,
        2: authentication_controller,
        3: listing_branch_controller,
        4: finish_program,
    }

    select = input("Выберите пункт меню: ")
    result = int(select) if select.isdigit() and 0 < int(select) <= len(actions) else len(actions)
    actions[result]()


logout()
return_to_main_menu()
