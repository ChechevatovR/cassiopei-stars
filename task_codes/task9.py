# -*- coding: utf-8 -*-

import random
import datetime
from flask import current_app


def task9_generator(team_id: int):
    days = random.randint(1, 3650001)
    d1 = datetime.date.fromordinal(days).strftime("%d.%m.%Y")
    d2 = datetime.date.fromordinal(days + 701).strftime("%d.%m.%Y")
    return d1, d2


with current_app.app_context():
    current_app.config['tasks'][9].generator = task9_generator
