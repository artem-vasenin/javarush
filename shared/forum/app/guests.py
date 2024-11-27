from bs4 import BeautifulSoup as bs4
import requests


class Guest:
    def __init__(self):
        pass

    def read_forum(self, url='http://127.0.0.1/forum/branches/'):
        """
        Метод "ходит" по всем доступным branche и сообщает об этом
        """
        response = requests.get(url)
        response.encoding = 'utf-8'
        soup = bs4(response.text, 'lxml')
        branches = soup.find_all('a', href=True)
        for branche in branches:
            generate_url = url+branche['href']
            requests.get(generate_url)
            print(f'Я прочитал ветку форума {branche.text.replace('/', '')} по ссылке {generate_url}')



    def registration(self):
        pass

    def authentication(self):
        pass


test = Guest()
test.read_forum()