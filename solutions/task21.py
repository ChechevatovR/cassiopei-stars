# -*- coding: utf-8 -*-
import requests

login = 'admin'
token = '2213ba90d3c8bba6de5ef0003a6dcab681c043ca6e2c474cea387a4c74e7eaae'
host = 'http://localhost/'


def send_data():
    print(f'Sending a POST request with...   ', end='', )
    text = requests.post(
        host + 'tasks/task21',
        cookies={'login': login, 'token': token, 'tea': '123'})
    print('Got a response')
    return text


def solve(text: str) -> int:
    return int(eval(text))


if __name__ == '__main__':
    send_data()