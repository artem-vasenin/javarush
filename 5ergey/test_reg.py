import random
import hashlib
import datetime
import os.path
import time

class Person:
    def __init__(self, username, password, secretkey=''):
        self.username = username
        self.password = password
        self.__hash = hashlib.md5(self.password.encode()).hexdigest()
        self.__secretkey = secretkey

    def registration(self):
        file_path = 'C:\\Users\\user\\Desktop\\users\\'
        if os.path.isfile(f'{file_path}{self.username}.txt'):
            print(f'Пользователь {self.username} уже существует. Придумайте другое имя')
            return False
        else:
            self.registration_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data_list = [self.username, self.__hash, self.__secretkey, self.registration_date]
            with open(f'{file_path}{self.username}.txt', 'w', encoding="utf-8") as file:
                for row in data_list:
                    file.write(row)
                    file.write("\n")
            return True

usernames_list = []
with open('femalenames-usa-top1000.txt', 'r', encoding="utf-8") as file:
    for name in file.readlines():
        usernames_list.append(name.lower().replace('\n', ''))

passwords_list = []
with open('500-worst-passwords.txt', 'r', encoding="utf-8") as file:
    for password in file.readlines():
        passwords_list.append(password.replace('\n', ''))

registered_users = {}
while len(registered_users) != 1000:
    random_name = random.choice(usernames_list)
    random_password = random.choice(passwords_list)
    new_user = Person(random_name, random_password)
    if new_user.registration():
        registered_users[new_user.username] = new_user
        print(f'Пользователь {new_user.username} зарегистирован')
        time.sleep(10)


