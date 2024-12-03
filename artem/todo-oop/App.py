class App:
    def __init__(self):
        self.mode = 'menu'
        self.menu = {
            1: {'title': 'Показать список задач', 'action': self.get_todos},
            2: {'title': 'Добавить задачу', 'action': self.add_todo},
            3: {'title': 'Пометить задачу выполненной', 'action': self.check_todo},
            4: {'title': 'Удалить задачу', 'action': self.remove_todo},
            5: {'title': 'Завершить программу', 'action': self.finish},
        }

    def get_menu(self) -> None:
        print(*[f'{k}: {v['title']}' for k, v in self.menu.items()], sep='\n')
        chose = input('Введите номер пункта меню: ')
        self.menu[int(chose)]['action']() if int(chose) in self.menu else print('Ошибка ввода')

    def get_todos(self):
        pass

    def add_todo(self):
        pass

    def check_todo(self):
        pass

    def remove_todo(self):
        pass

    def finish(self):
        pass