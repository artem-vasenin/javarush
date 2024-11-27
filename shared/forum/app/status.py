

class Status:
    def __init__(self):
        self.stat = {"user":{}, "branch": {}}

    def status_registration(self, name, role):
        self.stat["user"] = {"login": name, "role": role}

    def status_branch(self, branch, count):
        self.stat["branch"][count] = branch

statu = Status()