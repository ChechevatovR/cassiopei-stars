# -*- coding: utf-8 -*-
import requests
import subprocess
from PIL import Image

login = 'admin'
token = '3cff426f1a92e50c811c9ac16f093bb41b92c0933374eee002d5f6b0345d106f'

host = 'http://localhost/'
# host = 'https://fetefot763.eu.pythonanywhere.com/'

marker_beg = '<div id="task-data">'
marker_end = '</div>'


class Vector:               # Опишем класс вектора для удобства
    x: int
    y: int

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def simplize(self):     # Метод, где координаты вектора уменьшаем до 1, сохраняя знак
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
    x1, y1, x2, y2 = None, None, None, None  # Координаты x y для первого и второго пикселей

    for x in range(img.size[0]):
        for y in range(img.size[1]):
            if pix[x, y] == (0, 0, 0):
                if x1 == None:      # Находим координаты первого чёрного пикселя
                    x1 = x
                    y1 = y
                else:               # Находим координаты второго чёрного пикселя
                    x2 = x
                    y2 = y
    vec = Vector(x2 - x1, y2 - y1)  # Создаём вектор с началом в первом пикселе и концов во втором
    vec.simplize()                  # Упрощаем его до вектора с координатами только 1, -1, или 0

    """
    Т.к. у нас записаны координаты только верхних левых углов пикселя, нам нужно определить 
    по расположению пикселей, какие углы нужны для вычисления расстояния (См. условие)
    В зависимости от четверти, в которой лежит вектор, меняем x1, y1, x2, y2
    """
    if vec.x == 1 and vec.y == 1: x1 += 1; y1 += 1
    if vec.x == -1 and vec.y == 1: y1 += 1; x2 += 1
    if vec.x == 1 and vec.y == -1: x1 += 1; y2 += 1
    if vec.x == -1 and vec.y == -1: x2 += 1; y2 += 1

    # Рассмотрим частные случаи, когда пиксели расположены на одной высоте или ровно друг под другом
    if vec.x == 0 and vec.y == 1: y1 += 1
    if vec.x == 0 and vec.y == -1: y2 += 1
    if vec.y == 0 and vec.x == 1: x1 += 1
    if vec.y == 0 and vec.x == -1: x2 += 1

    # Вычисляем искомое расстояние, через формулу расстояний между точками
    length = ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5
    round_len = round(length, 5)    # Округляем до 5 знаков
    if int(length) != length:       # Отбрасываем ".0", если он присутствует
        ans = str(round_len)
    else:
        ans = str(int(round_len))
    return ans


if __name__ == '__main__':
    while True:
        get_data()
        send_data(solve())
