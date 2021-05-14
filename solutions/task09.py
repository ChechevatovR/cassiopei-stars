# -*- coding: utf-8 -*-
import requests
import datetime

login = 'admin'
# token = '6bdfaa4659236b37944dadeb3727565b484ac206ad15f71b5427b91685aec959'
token = '6dc95cf8121d37505ac92bf9e0313ad46517b1121709237216230e756148c709'
host = 'http://localhost/'
# host = 'https://fetefot763.eu.pythonanywhere.com/'

marker_beg = '<div id="task-data">'
marker_end = '</div>'


def get_data():
    print('Sending a GET request...   ', end='')
    text = requests.get(
        host + 'tasks/task9',
        cookies={'login': login, "token": token},
        allow_redirects=False
    ).text
    # print(text)
    print('Got a response')
    return text


def send_data(data):
    print(f'Sending a POST request with "{data}"...   ', end='', )
    text = requests.post(
        host + 'tasks/task9',
        cookies={'login': login, "token": token},
        data={'answer': data},
        allow_redirects=False
    ).text
    print('Got a response')
    return text


def get_text_from_data(data: str) -> str:
    ind_beg = data.rfind(marker_beg) + len(marker_beg)
    ind_end = data[ind_beg:].find(marker_end)
    text = data[ind_beg:ind_beg + ind_end].strip()
    return text


def solve(text: str) -> str:
    days = datetime.datetime.strptime(text, '%d.%m.%Y').date().toordinal()
    days += 701
    return datetime.date.fromordinal(days).strftime('%d.%m.%Y')


if __name__ == '__main__':
    while True:
        txt = get_text_from_data(get_data())
        print(txt)
        res = solve(txt)
        send_data(res)

