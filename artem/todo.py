bd = []

def get_todos():
    pass

def add_todo():
    pass

def check_todo(id: str):
    pass

def remove_todo(id: str):
    pass

settings = {
    'mode': 'menu',
    'menu': {
        1: 'Показать список задач',
        2: 'Добавить задачу',
        3: 'Пометить задачу выполненной',
        4: 'Удалить задачу',
    },
    'menu_actions': {
        '1': get_todos,
        '2': add_todo,
        '3': check_todo,
        '4': remove_todo,
    }
}

def get_menu():
    print(*[f'{k}: {v}' for k, v in settings['menu'].items()], sep='\n')
    chose = input('Введите номер пункта меню: ')
    settings['menu_actions'][chose]() if chose in settings['menu_actions'] else print('Ошибка ввода')

def render_todo():
    if settings['mode'] == 'menu':
        get_menu()

render_todo()