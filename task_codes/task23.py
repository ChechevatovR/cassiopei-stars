# -*- coding: utf-8 -*-

import random
from flask import current_app


def task23_generator(team_id: int):
    with open('task-static-content/wordlist.txt', 'r') as wordlist:
        words = [i[:-1] for i in wordlist.readlines()]

    text = ''
    while len(text) < 2500:
        text += random.choice(words)
        text += ' '
    return text, task23_solve(text)


def task23_solve(text: str) -> str:
    with open('task-static-content/chemlist.txt', 'r') as chemlist:
        chem = [i[:-1].lower().split(',') for i in chemlist.readlines()]
    chem.sort(key=lambda x: len(x[1]), reverse=True)
    for elem in chem:
        text = text.replace(elem[1], elem[0])
    return text


with current_app.app_context():
    current_app.config['tasks'][23].generator = task23_generator