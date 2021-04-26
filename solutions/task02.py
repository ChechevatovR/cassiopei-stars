# -*- coding: utf-8 -*-
import requests
import subprocess

login = 'solve'
# token = '7ce14d7948e51ff28b45c34be89fd71b0913f554f725143208c8bc9da4f9d66a'
token = '23847634320439b65adafb7e3fefff802b1cde0a1b2977c3fe299a6dd111e4ce'
# host = 'http://localhost/'
host = 'https://fetefot763.eu.pythonanywhere.com/'

marker_beg = '<div id="task-data">'
marker_end = '</div>'


def get_data():
    print('Sending a GET request...   ', end='')
    text = requests.get(
        host + 'tasks/task2',
        cookies={'login': login, "token": token},
        allow_redirects=False
    ).text
    with open('2.zip', 'wb') as archive:
        archive.write(
            requests.get(
                host + 'task-generated-content/2/task2_8.zip',
                cookies={'login': login, "token": token},
                    allow_redirects=False
            ).content
        )
    print('Got a response')


def send_data(data):
    print(f'Sending a POST request with "{data}"...   ', end='', )
    text = requests.post(
        host + 'tasks/task2',
        cookies={'login': login, "token": token},
        data={'answer': data},
        allow_redirects=False
    ).text
    print('Got a response')


def solve() -> str:
    subprocess.call(['tar',  '-xf',  '2.zip'])
    with open('answer.txt', 'r') as res:
        return res.read()


if __name__ == '__main__':
    while True:
        get_data()
        res = solve()
        send_data(solve())

