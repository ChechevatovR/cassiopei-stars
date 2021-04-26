# -*- coding: utf-8 -*-
import requests

login = 'admin'
token = 'ba3d78ada33a09d5e235263bf773a50a4f10c076830951c372d552806024d734'
host = 'http://localhost/'
# host = 'https://fetefot763.eu.pythonanywhere.com/'

marker_beg = '<div id="task-data">'
marker_end = '</div>'


def get_data():
    print('Sending a GET request...   ', end='')
    text = requests.get(
        host + 'tasks/task4',
        cookies={'login': login, "token": token},
        allow_redirects=False
    ).text
    print('Got a response')
    return text


def send_data(data):
    print(f'Sending a POST request with "{data}"...   ', end='', )
    text = requests.post(
        host + 'tasks/task4',
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
    return text


def solve(text: str) -> str:
    return text \
        .replace('🤣🤣🤣', 'rofl') \
        .replace('🤣🤣', 'rofl') \
        .replace('🤣', 'rofl') \
        .replace('🤔🤔🤔', 'ooo_OOO') \
        .replace('🤔🤔', 'oo_OO') \
        .replace('🤔', 'o_O') \
        .replace('🤑🤑🤑', '$$$_$$$') \
        .replace('🤑🤑', '$$_$$') \
        .replace('🤑', '$_$') \
        .replace('🙂🙂🙂', '=)))') \
        .replace('🙂🙂', '=))') \
        .replace('🙂', '=)') \
        .replace('🙁🙁🙁', '=(((') \
        .replace('🙁🙁', '=((') \
        .replace('🙁', '=(') \
        .replace('😕😕😕', '=///') \
        .replace('😕😕', '=//') \
        .replace('😕', '=/') \
        .replace('😑😑😑', '---_---') \
        .replace('😑😑', '--_--') \
        .replace('😑', '-_-') \
        .replace('😉😉😉', ';)))') \
        .replace('😉😉', ';))') \
        .replace('😉', ';)') \
        .replace('😂😂😂', 'XDDD') \
        .replace('😂😂', 'XDD') \
        .replace('😂', 'XD')


if __name__ == '__main__':
    while True:
        txt = get_text_from_data(get_data())
        res = solve(txt)
        send_data(res)

