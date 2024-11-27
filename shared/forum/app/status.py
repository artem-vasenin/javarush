

class Status:
    def __init__(self):
        self.stat = {"user":{}, "branch":None}

    def status_registration(self, name, role):
        self.stat["user"] = {"login": name, "role": role}

    def status_branch(self, branch):
        self.stat["branch"] = branch

statu = Status()