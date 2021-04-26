# -*- coding: utf-8 -*-
import requests
import subprocess
from PIL import Image

login = 'admin'
token = '3d61e23fa4a5730860db8ffb668ef53799e66163a69c78c37acfb7eec71692f5'

host = 'http://localhost/'
#host = 'https://fetefot763.eu.pythonanywhere.com/'

marker_beg = '<div id="task-data">'
marker_end = '</div>'


def get_data():
    print('Sending a GET request...   ', end='')
    text = requests.get(
        host + 'tasks/task29',
        cookies={'login': login, "token": token},
        allow_redirects=False
    ).text
    with open('29.png', 'wb') as archive:
        archive.write(
            requests.get(
                host + 'task-generated-content/29/task29_1.png',
                cookies={'login': login, "token": token},
                    allow_redirects=False
            ).content
        )
    print('Got a response')


def send_data(data1, data2, data3):
    # print(f'Sending a POST request with "{data}"...   ', end='', )
    text = requests.post(
        host + 'tasks/task29',
        cookies={'login': login, "token": token},
        data={'answer1': data1, 'answer2': data2, 'answer3': data3},
        allow_redirects=False
    ).text
    print('Got a response')


def solve() -> str:
    img = Image.open('29.png')
    pix = img.load()
    return (255 - pix[0, 0][0], 255 - pix[0, 0][1], 255 - pix[0, 0][2])


if __name__ == '__main__':
    while True:
        get_data()
        res = solve()
        send_data(res[0], res[1], res[2])

