# -*- coding: utf-8 -*-
import requests
import subprocess
from PIL import Image

login = 'admin'
token = '3cff426f1a92e50c811c9ac16f093bb41b92c0933374eee002d5f6b0345d106f'

host = 'http://localhost/'
#host = 'https://fetefot763.eu.pythonanywhere.com/'

marker_beg = '<div id="task-data">'
marker_end = '</div>'


class vector():
    x: int
    y: int

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def normalize(self):
        if self.x != 0: self.x = self.x // abs(self.x)
        if self.y != 0: self.y = self.y // abs(self.y)


def get_data():
    print('Sending a GET request...   ', end='')
    text = requests.get(
        host + 'tasks/task43',
        cookies={'login': login, "token": token},
        allow_redirects=False
    ).text
    with open('43.png', 'wb') as archive:
        archive.write(
            requests.get(
                host + 'task-generated-content/43/task43_1.png',
                cookies={'login': login, "token": token},
                    allow_redirects=False
            ).content
        )
    print('Got a response')


def send_data(data):
    print(f'Sending a POST request with "{data}"...   ', end='', )
    text = requests.post(
        host + 'tasks/task43',
        cookies={'login': login, "token": token},
        data={'answer': data},
        allow_redirects=False
    ).text
    print('Got a response')


def solve() -> str:
    img = Image.open('43.png')
    pix = img.load()
    x1, y1, x2, y2 = None, None, None, None

    for x in range(img.size[0]):
        for y in range(img.size[1]):
            if pix[x,y] == (0, 0, 0):
                if x1 == None:
                    x1 = x
                    y1 = y
                else:
                    x2 = x
                    y2 = y
    vec = vector(x2 - x1, y2 - y1)
    vec.normalize()
    #print(f'direction -> ({vec.x}, {vec.y})')

    if vec.x == 1 and vec.y == 1: x1 += 1; y1 += 1
    if vec.x == -1 and vec.y == 1: y1 += 1; x2 += 1
    if vec.x == 1 and vec.y == -1: x1 += 1; y2 += 1
    if vec.x == -1 and vec.y == -1: x2 += 1; y2 += 1

    if vec.x == 0 and vec.y == 1: y1 += 1
    if vec.x == 0 and vec.y == -1: y2 += 1
    if vec.y == 0 and vec.x == 1: x1 += 1
    if vec.y == 0 and vec.x == -1: x2 += 1

    #print(f'width: {abs(x2-x1)}; height: {abs(y2-y1)}')
    length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    #print('l =', length)
    round_len = round(length, 5)
    if int(length) != length:
        ans = str(round_len)
    else:
        ans = str(int(round_len))
    #print('Answer:', ans)


    return ans


if __name__ == '__main__':
    while True:
        get_data()

        send_data(solve())

