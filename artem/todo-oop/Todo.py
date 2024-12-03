from datetime import datetime

class Todo:
    def __init__(self, title):
        self.id = datetime.timestamp(datetime.now())
        self.title = title
        self.date = datetime.now()
        self.isFinished = False

    def add_to_db(self):
        print('save todo')

    def get_list_from_db(self):
        print('get list')

    def remove_from_db(self):
        print('get list')

    def set_finished(self):
        print('set finished')