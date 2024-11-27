

class Status:
    def __init__(self):
        self.stat = {}

    def regist(self, name, role):
        self.stat["user"] = {"name": name, "role": role}

statu = Status()