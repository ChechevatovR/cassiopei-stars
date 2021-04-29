# -*- coding: utf-8 -*-
import requests
import time

login = 'admin'
# token = '37d62656f79a72da9cd293aaea21a848fa7bdaad03ee7e9224be9197dd758dcd'
token = '7c50ce806271c19e07d69f71fb89890aa08ce7cc153dc209c27a32e8609d0d66'
# host = 'http://localhost/'
host = 'https://fetefot763.eu.pythonanywhere.com/'

marker_beg = '<div id="task-data">'
marker_end = '</div>'


def get_data():
    print('Sending a GET request...   ', end='')
    start = time.time()
    text = requests.get(
        host + 'tasks/task1',
        cookies={'login': login, "token": token},
        allow_redirects=False
    ).text
    #print(text)
    print(f'Got a response in {time.time() - start}')
    return text


def send_data(data):
    print(f'Sending a POST request with "{data}"...   ', end='')
    start = time.time()

    text = requests.post(
        host + 'tasks/task1',
        cookies={'login': login, "token": token},
        data={'answer': data},
        allow_redirects=False
    ).text
    print(f'Got a response in {time.time() - start}')
    return text


def get_text_from_data(data: str) -> str:
    ind_beg = data.rfind(marker_beg) + len(marker_beg)
    ind_end = data[ind_beg:].find(marker_end)
    text = data[ind_beg:ind_beg + ind_end]
    # print(text)
    return text


def solve(text: str) -> int:
    text = text.replace('\r', ' ')
    text = text.replace('\n', ' ')
    text = text.replace('.', ' ')
    text = text.replace(',', ' ')
    text = text.replace('!', ' ')
    text = text.replace('?', ' ')
    text = text.replace('-', ' ')
    #while '  ' in text:
    #    text = text.replace('  ', ' ')
    text = text.strip()
    # print(text.split())
    return len(text.split())


if __name__ == '__main__':
    start = time.time()
    sols = 0
    while True:
        txt = get_text_from_data(get_data())
        res = solve(txt)
        # print(res, txt)
        send_data(res)
        sols += 1
        print(f'AVERAGE: {round((time.time() - start) / sols, 5)} sec/sols ON {sols} solutions')

