# -*- coding: utf-8 -*-
import requests
import time

login = 'admin'
token = 'e02b01fea34d12dfc54ffa8bbd5cd0230b2d75ec970f5bda893f50f4d5b40f09'
host = 'http://localhost/'

marker_beg = '<div id="task-data">'
marker_end = '</div>'


staff = dict()
with open('14.csv') as file:
    for line in file.readlines():
        man = line[:-1].split(',')
        staff[' '.join([man[0], '...', man[2]])] = man[1]
        staff[' '.join([man[0], man[1], '...'])] = man[2]
# print(staff, sep='\n')


def get_data():
    print('Sending a GET request...   ', end='')
    start = time.time()
    text = requests.get(
        host + 'tasks/task14',
        cookies={'login': login, "token": token},
        allow_redirects=False
    ).text
    # print(text)
    print(f'Got a response in {time.time() - start}')
    return text


def send_data(data):
    print(f'Sending a POST request with "{data}"...   ', end='')
    start = time.time()

    text = requests.post(
        host + 'tasks/task14',
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
    print(text)
    return text


def solve(text):
    return staff[text]


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

