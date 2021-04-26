from shared import *
from flask import current_app
import random


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


with current_app.app_context():
    current_app.config['tasks'][4].generator = task4_generator
