# -*- coding: utf-8 -*-
import requests

login = 'admin'
token = '6dc95cf8121d37505ac92bf9e0313ad46517b1121709237216230e756148c709'
host = 'http://localhost/'


def send_data():
    print(f'Sending a POST request with...   ', end='', )
    text = requests.post(
        host + 'tasks/task21',
        cookies={'login': login, 'token': token, 'tea': 'tea'})
    print('Got a response')
    return text


if __name__ == '__main__':
    send_data()