# -*- coding: utf-8 -*-

from flask import current_app
import random


def task14_generator(team_id: int):
    with open('task-static-content/14.csv', 'r') as workers_list:
        workers = [i[:-1].split(',') for i in workers_list.readlines()]
    worker = random.choice(workers)[:]
    forget = random.randint(1, 2)
    # print(worker, forget)
    answer = worker[forget]
    worker[forget] = '...'
    return ' '.join(worker), answer


with current_app.app_context():
    current_app.config['tasks'][14].generator = task14_generator
