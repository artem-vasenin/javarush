import os
class RunServer:
    def __init__(self, path=os.getcwd(), port=80):
        self.path = path
        self.port = port

    def start(self):
        """
        Метод запускает http.server в указанной директории и на указанном порту
        """
        os.system(f"python -m http.server --directory {self.path} --bind 127.0.0.1 {self.port}")


http_server_80 = RunServer('../../')
http_server_80.start()