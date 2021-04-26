# -*- coding: utf-8 -*-
import requests

login = 'admin'
token = 'd5475d8022feeff00efed28421c3ef56a028687c2e58303d076f2cccded8883b'
host = 'http://localhost/'
# host = 'https://fetefot763.eu.pythonanywhere.com/'

marker_beg = '<div id="task-data">'
marker_end = '</div>'


def get_data():
    print('Sending a GET request...   ', end='')
    text = requests.get(
        host + 'tasks/task1',
        cookies={'login': login, "token": token},
        allow_redirects=False
    ).text
    #print(text)
    print('Got a response')
    return text


def send_data(data):
    print(f'Sending a POST request with "{data}"...   ', end='', )
    text = requests.post(
        host + 'tasks/task1',
        cookies={'login': login, "token": token},
        data={'answer': data},
        allow_redirects=False
    ).text
    print('Got a response')
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
    print(text.split())
    return len(text.split())


if __name__ == '__main__':
    while True:
        txt = get_text_from_data(get_data())
        res = solve(txt)
        print(res, txt)
        send_data(res)

