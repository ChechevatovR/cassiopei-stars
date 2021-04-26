# -*- coding: utf-8 -*-

import random
from flask import current_app


def task1_generator(team_id: int):
    with open('task-static-content/wordlist.txt', 'r') as wordlist:
        words = [i[:-1] for i in wordlist.readlines()]
    splitters = '.,-?!'
    text = ''
    answer = 0
    while len(text) < 1000:
        text += random.choice(words)
        answer += 1

        if random.random() < .15:
            if random.random() < .4:
                text += ' ' * random.randint(1, 5)
            text += random.choice(splitters)
            if random.random() < .4:
                text += ' ' * random.randint(1, 5)
        else:
            text += ' ' * random.randint(1, 5)
    return text, answer


with current_app.app_context():
    current_app.config['tasks'][1].generator = task1_generator