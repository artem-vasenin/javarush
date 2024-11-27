class State:
    def __init__(self):
        self.state: dict = {
            "user":{},
            "branch": {}
        }

    def set_user(self, name: str, role: str) -> None:
        self.state["user"] = { "login": name, "role": role }

    def set_branch(self, branch, count):
        self.state["branch"][count] = branch

    def get_user(self):
        return self.state["user"]

    def get_branch(self):
        return self.state["branch"]

state = State()