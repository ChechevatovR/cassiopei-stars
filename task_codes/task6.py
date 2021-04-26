from flask import current_app
import random

MATH_RANGE = 10**9


def task6_generator(team_id: int):
    answer = random.randint(-MATH_RANGE, MATH_RANGE)
    return task6_generate_math(answer, 1), answer


def task6_generate_math(res: int, depth) -> str:
    if depth < 10:
        return random.choice([task6_gen_add, task6_gen_sub, task6_gen_mul, task6_gen_div])(res, depth + 1)
    return str(res)


def task6_gen_add(res: int, depth: int) -> str:
    l = random.randint(-MATH_RANGE, MATH_RANGE)
    r = res - l
    ls = task6_generate_math(l, depth)
    rs = task6_generate_math(r, depth)
    return f'({ls})+({rs})'


def task6_gen_sub(res: int, depth: int) -> str:
    l = random.randint(-MATH_RANGE, MATH_RANGE)
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


with current_app.app_context():
    current_app.config['tasks'][6].generator = task6_generator
