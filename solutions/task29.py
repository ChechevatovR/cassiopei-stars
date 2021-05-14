# -*- coding: utf-8 -*-
import requests
import subprocess
from PIL import Image

login = 'admin'
token = '6dc95cf8121d37505ac92bf9e0313ad46517b1121709237216230e756148c709'

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


def send_data(data):
    print(f'Sending a POST request with "{data}"...   ', end='', )
    text = requests.post(
        host + 'tasks/task29',
        cookies={'login': login, "token": token},
        data={'answer': data},
        allow_redirects=False
    ).text
    print('Got a response')


def solve() -> str:
    img = Image.open('29.png')
    pix = img.load()
    return '#' + ''.join(map(lambda colour: hex(255 - colour)[2:].upper().zfill(2), pix[0, 0]))


if __name__ == '__main__':
    while True:
        get_data()
        res = solve()
        send_data(res)

