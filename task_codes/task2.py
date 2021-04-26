from shared import *
from flask import current_app
import subprocess
import random
import os


def task2_generator(team_id: int):
    with open('task-static-content/wordlist.txt', 'r') as wordlist:
        words = [i[:-1] for i in wordlist.readlines()]
    pl = ' '.join(random.choices(words, k=5))
    with open(f'./task-generated-content/2/answer.txt', 'w') as pl_file:
        pl_file.write(pl)

    for i in range(5):
        with open(f'./task-generated-content/2/{i}.txt', 'w') as trash_file:
            trash_file.write(' '.join(random.choices(words, k=5)))

    filename = f'task2_{team_id}.zip'

    os.chdir('./task-generated-content/2')
    try:
        subprocess.run(['zip', f'{filename}', '0.txt', '1.txt', '2.txt', '3.txt', '4.txt', 'answer.txt'])
    except Exception as e:
        print(e)
        print('May be we are just on a Windows machine?..')
    os.chdir('./../../')

    return f'<a href="/task-generated-content/2/{filename}">archive.zip</a>', pl


with current_app.app_context():
    current_app.config['tasks'][2].generator = task2_generator