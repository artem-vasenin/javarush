mode = 'menu'
db = []

def load_db() -> None:
    with open('db.txt') as f:
        global db
        db = []
        for i in [x.strip() for x in f]:
            line = i.split('|')
            dct = {'id': int(line[0]), 'title': line[1], 'isFinished': bool(int(line[2]))}
            db.append(dct)

def save_in_db() -> None:
    with open('db.txt', 'w') as f:
        lst = []
        for i in [x for x in db]:
            lst.append(f'{i['id']}|{i['title']}|{int(i['isFinished'])}\n')
        f.writelines(lst)

def print_todos(lst):
    print('='*100)
    if len(lst):
        for i in range(len(lst)):
            print(f'| ID: {lst[i]["id"]} | "{lst[i]['title']}" {"| (Завершена)" if lst[i]['isFinished'] else ""}')
            if len(lst)-1 != i:
                print('-'*100)
    else:
        print('Записей пока нет. Самое время добавить!')
    print('='*100)

def get_todos():
    load_db()
    print_todos(db)

def add_todo():
    title = input('Введите заголовок: ')
    idx = max([e["id"] for e in db]) + 1 if db else 1
    db.append({'id': int(idx), 'title': title, 'isFinished': False})
    save_in_db()
    print('Запись успешно добавлена')
    print_todos(db)

def check_todo():
    idx = int(input('Введите ID задачи которую хотите завершить: '))
    result = [e for e in db if e['id'] == idx]
    if len(result):
        result[0]['isFinished'] = True
        save_in_db()
        print('Запись обновлена')
        print_todos(db)
    else:
        print('Записи с таким ID в списке нет', end='\n\n')

def remove_todo():
    global db
    idx = input()
    if idx.isdigit() and int(idx) in [e['id'] for e in db]:
        db = [e for e in db if e['id'] != int(idx)]
        save_in_db()
        print(f'Запись с ID: {idx} успешно удалена')
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