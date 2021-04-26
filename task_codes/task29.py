import random
from flask import current_app
from PIL import Image


def task29_generator(team_id: int):
    filepath = f'task-generated-content/29/task29_{team_id}.png'
    colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    img = Image.new("RGB", (2,2), colour)
    img.save(filepath, "PNG")

    req_colour = (255-colour[0], 255-colour[1], 255-colour[2])
    return f'<img src=/{filepath} width=100%>', str(req_colour)


with current_app.app_context():
    current_app.config['tasks'][29].generator = task29_generator
