from State import State
import datetime

state = State()

class App:
    def __init__(self):
        self.menu = {
            1: {'title': 'Показать список задач', 'action': self.get_todos},
            2: {'title': 'Добавить задачу', 'action': self.add_todo},
            3: {'title': 'Пометить задачу выполненной', 'action': self.check_todo},
            4: {'title': 'Удалить задачу', 'action': self.remove_todo},
        }

    def get_menu(self) -> None:
        print(*[f'{k}: {v['title']}' for k, v in self.menu.items()], sep='\n')
        chose = input('Введите номер пункта меню: ')

        if chose.isdigit() and int(chose) <= len(self.menu):
            self.menu[int(chose)]['action']()
        else:
            print('-'*32, 'Данные не верны. Повторите ввод:', '-'*32, sep='\n')
            self.get_menu()

    @staticmethod
    def print_todos(lst: list[dict]) -> None:
        print('=' * 100)
        if len(lst):
            for i in range(len(lst)):
                print(
                    f'| ID: {lst[i]["id"]} | Date: {lst[i]["date"]} | "{lst[i]['title']}" {"| (Завершена)" if lst[i]['isFinished'] else ""}')
                if len(lst) - 1 != i:
                    print('-' * 100)

    def get_todos(self):
        try:
            state.load_db()
            self.print_todos(state.db)
        except FileNotFoundError:
            print('-'*50, 'База данных не найдена...', '-'*50, sep='\n')

    def add_todo(self):
        try:
            state.load_db()
        except FileNotFoundError:
            pass

        def dt_format(n: int) -> str:
            return str(n) if n > 9 else f'0{n}'

        title = input('Введите заголовок: ')
        idx = max([e["id"] for e in state.db]) + 1 if state.db else 1
        dt = datetime.datetime.now()
        day = dt_format(dt.day)
        month = dt_format(dt.month)
        hour = dt_format(dt.hour)
        minute = dt_format(dt.minute)
        state.db.append({'id': int(idx), 'date': f'{day}/{month}/{dt.year} {hour}:{minute}', 'title': title, 'isFinished': False})
        state.save_in_db()
        self.print_todos(state.db)

    def check_todo(self):
        idx = input('Введите ID задачи которую хотите завершить: ')
        if idx.isdigit():
            elem = state.find_by_id(int(idx))
            if elem:
                elem['isFinished'] = True
                state.update_element(elem)
                self.print_todos(state.db)
        else:
            print('Неверные данные, попробуйте снова:')
            self.check_todo()

    def remove_todo(self):
        idx = input('Введите ID задачи которую хотите удалить: ')
        if idx.isdigit():
            state.delete_element(int(idx))
            self.print_todos(state.db)
        else:
            print('Неверные данные, попробуйте снова:')
            self.remove_todo()