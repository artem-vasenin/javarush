db = [
    {'id': 1, 'title': 'купить хлеб', 'isFinished': False},
]
mode = 'menu'

def print_todos(lst):
    print('='*100)
    for i in range(len(lst)):
        print(f'| ID: {lst[i]["id"]} | "{lst[i]['title']}" {"| (Завершена)" if lst[i]['isFinished'] else ""}')
        if len(lst)-1 != i:
            print('-'*100)
    print('='*100)

def get_todos():
    print_todos(db)

def add_todo():
    title = input('Введите заголовок: ')
    id = max([e["id"] for e in db]) + 1
    db.append({'id': int(id), 'title': title, 'isFinished': False})
    print('Запись успешно добавлена')
    print_todos(db)

def check_todo():
    id = int(input('Введите ID задачи которую хотите завершить: '))
    result = [e for e in db if e['id'] == id]
    if len(result):
        result[0]['isFinished'] = True
        print('Запись обновлена')
        print_todos(db)
    else:
        print('Записи с таким ID в списке нет', end='\n\n')

def remove_todo():
    global db
    id = input()
    if id.isdigit() and int(id) in [e['id'] for e in db]:
        db = [e for e in db if e['id'] != int(id)]
        print(f'Запись с ID: {id} успешно удалена')
        print_todos(db)
    else:
        print('Введен неверный ID или записи с таким ID в списке нет')

def finish():
    global mode
    print('============= Bye-bye! =============')
    mode = 'finished'

settings = {
    'menu': {
        1: 'Показать список задач',
        2: 'Добавить задачу',
        3: 'Пометить задачу выполненной',
        4: 'Удалить задачу',
        5: 'Завершить программу',
    },
    'menu_actions': {
        '1': get_todos,
        '2': add_todo,
        '3': check_todo,
        '4': remove_todo,
        '5': finish,
    }
}

def get_menu():
    print(*[f'{k}: {v}' for k, v in settings['menu'].items()], sep='\n')
    chose = input('Введите номер пункта меню: ')
    settings['menu_actions'][chose]() if chose in settings['menu_actions'] else print('Ошибка ввода')

def render_todo():
    while mode == 'menu':
        get_menu()

render_todo()