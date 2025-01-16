class State:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.mode = 'menu'
        self.db = []

    def save_in_db(self) -> None:
        with open('db.txt', 'w') as f:
            lst = []
            for i in [x for x in self.db]:
                lst.append(f'{i['id']}|{i['date']}|{i['title']}|{int(i['isFinished'])}\n')
            f.writelines(lst)
        print('База данных обновлена')

    def load_db(self) -> None:
        self.db = []
        with open('db.txt') as f:
            for i in [x.strip() for x in f]:
                line = i.split('|')
                dct = {'id': int(line[0]), 'date': line[1], 'title': line[2], 'isFinished': bool(int(line[3]))}
                self.db.append(dct)

    def find_by_id(self, idx: int):
        try:
            self.load_db()
        except FileNotFoundError:
            print('База данных пуста')
            return

        for el in self.db:
            if el['id'] == idx:
                return el


    def update_element(self, item) -> None:
        try:
            self.load_db()
        except FileNotFoundError:
            print('База данных пуста')
            return
        new_db = []
        for el in self.db:
            if el['id'] == item['id']:
                new_db.append(item)
            else:
                new_db.append(el)
        self.db = [*new_db]
        self.save_in_db()


    def delete_element(self, idx) -> None:
        try:
            self.load_db()
        except FileNotFoundError:
            print('База данных пуста')
            return

        self.db = list(filter(lambda x: x['id'] != idx, self.db))
        self.save_in_db()
