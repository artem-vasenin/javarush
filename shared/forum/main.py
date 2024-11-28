from shared.forum.menu import Beginning

beginning = Beginning()

if __name__=="__main__":
    beginning.print_menu()
    beginning.choose_action()


# def register_controller():
#     """ Вызов функции регистрации пользователя """
#     user.register()
#     print_menu()
#     choose_action()


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

# def authentication_controller():
#     """ Вызов функции входа в приложение """
#     users = guest.authentication()
#     beginning.print_menu(users)
#     beginning.choose_action(users)