import random
from shared_core import *
from flask import current_app, request
from PIL import Image, ImageDraw
import subprocess
import os
import datetime

TASK_6_RANGE = 1000


class Vector:
    x: int
    y: int

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def normalize(self):
        if self.x != 0:
            self.x = self.x // abs(self.x)
        if self.y != 0:
            self.y = self.y // abs(self.y)


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


def task4_generator(team_id: int):
    with open('task-static-content/wordlist.txt', 'r') as wordlist:
        words = [i[:-1] for i in wordlist.readlines()]
    emojis = "🙂🙁😕😉😑🤔🤑😂🤣"
    for duplicates in range(7):
        for l in range(1, 4):
            for emoji in emojis:
                words += [emoji * l]
    text = ''
    answer = 0
    while len(text) < 1880:
        text += random.choice(words)
        answer += 1
        text += ' '
    return text[:-1], task4_solve(text[:-1])


def task4_solve(text: str) -> str:
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


def task6_generator(team_id: int):
    answer = random.randint(-TASK_6_RANGE, TASK_6_RANGE)
    return task6_generate_math(answer, 1), answer


def task6_generate_math(res: int, depth) -> str:
    def task6_gen_add(res: int, depth: int) -> str:
        l = random.randint(-TASK_6_RANGE, TASK_6_RANGE)
        r = res - l
        ls = task6_generate_math(l, depth)
        rs = task6_generate_math(r, depth)
        return f'({ls})+({rs})'

    def task6_gen_sub(res: int, depth: int) -> str:
        l = random.randint(-TASK_6_RANGE, TASK_6_RANGE)
        r = l - res
        ls = task6_generate_math(l, depth)
        rs = task6_generate_math(r, depth)
        return f'({ls})-({rs})'

    def task6_gen_mul(res: int, depth: int) -> str:
        l = random.choice(task6_dividers(res))
        while l == 0:
            l = random.choice(task6_dividers(res))
        r = res // l
        ls = task6_generate_math(l, depth)
        rs = task6_generate_math(r, depth)
        return f'({ls})*({rs})'

    def task6_gen_div(res: int, depth: int) -> str:
        r = random.randint(-10, 10)
        while r == 0:
            r = random.randint(-10, 10)
        l = res * r
        ls = task6_generate_math(l, depth)
        rs = task6_generate_math(r, depth)
        return f'({ls})/({rs})'

    def task6_dividers(n: int) -> list:
        res = [1, n]
        i = 2
        while i * i <= n:
            if n % i == 0:
                res += [i]
                if i * i != n:
                    res += [n // i]
            i += 1
        return res

    if depth < 10:
        return random.choice([task6_gen_add, task6_gen_sub, task6_gen_mul, task6_gen_div])(res, depth + 1)
    return str(res)


def task9_generator(team_id: int):
    def adjust_date(text: str) -> str:
        l = text.split('.')
        l[0] = l[0].zfill(2)
        l[1] = l[1].zfill(2)
        l[2] = l[2].zfill(4)
        text = '.'.join(l)
        return text

    days = random.randint(1, 3650001)
    d1 = datetime.date.fromordinal(days).strftime("%d.%m.%Y")
    d2 = datetime.date.fromordinal(days + 701).strftime("%d.%m.%Y")
    return adjust_date(d1), adjust_date(d2)


def task14_generator(team_id: int):
    with open('task-static-content/14.csv', 'r') as workers_list:
        workers = [i[:-1].split(',') for i in workers_list.readlines()]
    worker = random.choice(workers)[:]
    forget = random.randint(1, 2)
    # print(worker, forget)
    answer = worker[forget]
    worker[forget] = '...'
    return ' '.join(worker), answer


def task15_checker(team_id: int):
    answer = request.form.get('answer')
    if answer is not None:  # Ответ нужно отправлять не через форму
        return False
    return True


def task21_checker(team_id: int):
    return 'tea' in [i.lower() for i in (list(request.cookies.keys()) + list(request.cookies.values()))]


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


def task27_generator(team_id: int):
    font = {
        '+': [
            r'_____________',
            r'_____________',
            r'_____/\\\____',
            r'____\/\\\____',
            r'_/\\\\\\\\\\\ ',
            r'\/////\\\///_',
            r'____\/\\\____',
            r'____\///_____',
            r'_____________',
        ],
        '-': [
            r'_____________',
            r'_____________',
            r'_____________',
            r'_/\\\\\\\\\\\ ',
            r'\///////////_',
            r'_____________',
            r'_____________',
            r'_____________',
            r'_____________'
        ],
        '*': [
            r'_______/\\\______',
            r'_/\\\_\/\\\__/\\\ ',
            r'\////\\\\\\\\\//_',
            r'___\////\\\//____',
            r'____/\\\\\\\\\___',
            r'_/\\\///\\\///\\\ ',
            r'\///__\/\\\_\///_',
            r'______\///_______',
            r'_________________',
        ],
        '=': [
            r'____________',
            r'____________',
            r'____________',
            r'_/\\\\\\\\\\',
            r'\//////////_',
            r'_/\\\\\\\\\\',
            r'\//////////_',
            r'____________',
            r'____________'
        ],
        '?': [
            r'____/\\\\\\\____',
            r'_/\\\//////\\\__',
            r'\///_____\//\\\_',
            r'__________/\\\__',
            r'_______/\\\\/___',
            r'______/\\\/_____',
            r'_____\///_______',
            r'______/\\\______',
            r'_____\///_______',
        ],
        '0': [
            r'_____/\\\\\\\__',
            r'___/\\\/////\\\ ',
            r'_/\\\____\//\\\ ',
            r'\/\\\_____\/\\\ ',
            r'\/\\\_____\/\\\ ',
            r'\/\\\_____\/\\\ ',
            r'\//\\\____/\\\_',
            r'_\///\\\\\\\/__',
            r'___\///////____'
        ],
        '1': [
            r'_____/\\\ ',
            r'_/\\\\\\\ ',
            r'\/////\\\ ',
            r'____\/\\\ ',
            r'____\/\\\ ',
            r'____\/\\\ ',
            r'____\/\\\ ',
            r'____\/\\\ ',
            r'____\///_ '
        ],
        '2': [
            r'___/\\\\\\\\\____',
            r'_/\\\///////\\\__',
            r'\///______\//\\\_',
            r'__________/\\\/__',
            r'_______/\\\//____',
            r'____/\\\//_______',
            r'__/\\\/__________',
            r'_/\\\\\\\\\\\\\\\ ',
            r'\///////////////_'
        ],
        '3': [
            r'____/\\\\\\\\\\_',
            r'__/\\\///////\\\ ',
            r'_\///______/\\\_',
            r'________/\\\//__',
            r'_______\////\\\_',
            r'__________\//\\\ ',
            r'_/\\\______/\\\_',
            r'\///\\\\\\\\\/__',
            r'__\/////////____'
        ],
        '4': [
            r'___________/\\\___',
            r'_________/\\\\\___',
            r'_______/\\\/\\\___',
            r'_____/\\\/\/\\\___',
            r'___/\\\/__\/\\\___',
            r'_/\\\\\\\\\\\\\\\\',
            r'\///////////\\\//_',
            r'__________\/\\\___',
            r'__________\///____'
        ],
        '5': [
            r'__/\\\\\\\\\\\\\\\ ',
            r'_\/\\\///////////_',
            r'_\/\\\____________',
            r'_\/\\\\\\\\\\\\___',
            r'_\////////////\\\_',
            r'____________\//\\\ ',
            r'_/\\\________\/\\\ ',
            r'\//\\\\\\\\\\\\\/_',
            r'_\/////////////___'
        ],
        '6': [
            r'___________/\\\\\ ',
            r'_______/\\\\////_',
            r'____/\\\///______',
            r'__/\\\\\\\\\\\___',
            r'_/\\\\///////\\\_',
            r'\/\\\______\//\\\ ',
            r'\//\\\______/\\\_',
            r'_\///\\\\\\\\\/__',
            r'___\/////////____'
        ],
        '7': [
            r'_/\\\\\\\\\\\\\\\ ',
            r'\/////////////\\\ ',
            r'___________/\\\/_',
            r'_________/\\\/___',
            r'_______/\\\/_____',
            r'_____/\\\/_______',
            r'___/\\\/_________',
            r'_/\\\/___________',
            r'\///_____________'
        ],
        '8': [
            r'____/\\\\\\\\\___',
            r'__/\\\///////\\\_',
            r'_\/\\\_____\/\\\_',
            r'_\///\\\\\\\\\/__',
            r'__/\\\///////\\\_',
            r'_/\\\______\//\\\ ',
            r'\//\\\______/\\\_',
            r'_\///\\\\\\\\\/__',
            r'___\/////////____'
        ],
        '9': [
            r'____/\\\\\\\\\___',
            r'__/\\\///////\\\_',
            r'_/\\\______\//\\\ ',
            r'\//\\\_____/\\\\\ ',
            r'_\///\\\\\\\\/\\\ ',
            r'___\////////\/\\\ ',
            r'_/\\________/\\\_',
            r'\//\\\\\\\\\\\/__',
            r'_\///////////____'
        ],
    }
    t = query_fetchone('SELECT in_row FROM task_status WHERE team_id = ? AND task_id = 27', [team_id])[0]
    s = f'{1000 - 7 * t}-7=?'
    lines = ['', '', '', '', '', '', '', '', '']
    for line in range(0, 9):
        lines[line] = '_' * line
        for char in s:
            lines[line] += font[char][line].strip() + '_'
    with open(f'task-generated-content/27/task27_{team_id}.txt', 'w') as file:
        for line in lines:
            file.write(line + '\n')
    return f'<a href="/task-generated-content/27/task27_{team_id}.txt">27.txt</a>', 1000 - 7 * (t + 1)


def task29_generator(team_id: int):
    filepath = f'task-generated-content/29/task29_{team_id}.png'

    colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    img = Image.new("RGB", (2, 2), colour)
    img.save(filepath, "PNG")
    answer = '#' + ''.join(map(lambda colour: hex(255 - colour)[2:].upper().zfill(2), colour))
    print(colour, answer)
    return f'<img src=/{filepath} width=100%>', answer


def task43_generator(team_id: int):
    filepath = f'task-generated-content/43/task43_{team_id}.png'
    height, width = 200, 200
    img = Image.new("RGB", (height, width), (255, 255, 255))
    x1, y1 = random.randint(0, width - 1), random.randint(0, height - 1)
    x2, y2 = random.randint(0, width - 1), random.randint(0, height - 1)
    while x2 == x1 and y2 == y1:
        x2, y2 = random.randint(0, width - 1), random.randint(0, height - 1)
    # print(x1,y1,'-',x2,y2)
    draw = ImageDraw.Draw(img)
    draw.point((x1, y1), (0, 0, 0))
    draw.point((x2, y2), (0, 0, 0))
    img.save(filepath, "PNG")

    vec = Vector(x2 - x1, y2 - y1)
    vec.normalize()
    # print(f'direction -> ({vec.x}, {vec.y})')

    if vec.x == 1 and vec.y == 1: x1 += 1; y1 += 1
    if vec.x == -1 and vec.y == 1: y1 += 1; x2 += 1
    if vec.x == 1 and vec.y == -1: x1 += 1; y2 += 1
    if vec.x == -1 and vec.y == -1: x2 += 1; y2 += 1

    if vec.x == 0 and vec.y == 1: y1 += 1
    if vec.x == 0 and vec.y == -1: y2 += 1
    if vec.y == 0 and vec.x == 1: x1 += 1
    if vec.y == 0 and vec.x == -1: x2 += 1

    length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    round_len = round(length, 5)
    if int(length) != length:
        ans = str(round_len)
    else:
        ans = str(int(round_len))
    return f'<img src=/{filepath} style="box-shadow: 0 0 10px rgba(0,0,0,0.5);">', ans


def task46_checker(team_id: int) -> bool:
    langs = [i.split(';') for i in request.headers.get('Accept-Language', 'ru').split(',')]
    for lang in langs:
        if len(lang) == 1:
            lang += [1]
            continue
        lang[1] = float(lang[1][2:])
    langs.sort(key=lambda i: -i[1])
    print(langs)
    return langs[0][0].startswith('en')

