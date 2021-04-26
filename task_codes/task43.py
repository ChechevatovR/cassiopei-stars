import random
from flask import current_app
from PIL import Image, ImageDraw


class Vector():
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

    if vec.x ==  1 and vec.y ==  1: x1 += 1; y1 += 1
    if vec.x == -1 and vec.y ==  1: y1 += 1; x2 += 1
    if vec.x ==  1 and vec.y == -1: x1 += 1; y2 += 1
    if vec.x == -1 and vec.y == -1: x2 += 1; y2 += 1

    if vec.x ==  0 and vec.y ==  1: y1 += 1
    if vec.x ==  0 and vec.y == -1: y2 += 1
    if vec.y ==  0 and vec.x ==  1: x1 += 1
    if vec.y ==  0 and vec.x == -1: x2 += 1

    # print(f'width: {abs(x2-x1)}; height: {abs(y2-y1)}')
    length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    # print('l =', length)
    round_len = round(length, 5)
    if int(length) != length:
        ans = str(round_len)
    else:
        ans = str(int(round_len))
    # print('Answer:', ans)
    return f'<img src=/{filepath} style="box-shadow: 0 0 10px rgba(0,0,0,0.5);">', ans


with current_app.app_context():
    current_app.config['tasks'][43].generator = task43_generator
