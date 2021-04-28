import random
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
    if depth < 10:
        return random.choice([task6_gen_add, task6_gen_sub, task6_gen_mul, task6_gen_div])(res, depth + 1)
    return str(res)


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


def task9_generator(team_id: int):
    days = random.randint(1, 3650001)
    d1 = datetime.date.fromordinal(days).strftime("%d.%m.%Y")
    d2 = datetime.date.fromordinal(days + 701).strftime("%d.%m.%Y")
    return d1, d2


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
    answer = request.form.get('answer')
    if answer is not None:  # Ответ нужно отправлять не через форму
        return False
    return 'tea' in [i.lower() for i in request.cookies.keys()]


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


def task29_generator(team_id: int):
    filepath = f'task-generated-content/29/task29_{team_id}.png'
    colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    img = Image.new("RGB", (2, 2), colour)
    img.save(filepath, "PNG")

    req_colour = (255 - colour[0], 255 - colour[1], 255 - colour[2])
    return f'<img src=/{filepath} width=100%>', str(req_colour)


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


# print('tasks', current_app)
# print('tasks', current_app.app_context)

