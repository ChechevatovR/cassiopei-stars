import sqlite3
import time

SCORE_PER_TASK = 1000


def query_fetchall(query_text: str, params=None):
    if params is None:
        params = []
    con = sqlite3.connect('db.sqlite')
    cursor = con.cursor()
    res = cursor.execute(query_text, params).fetchall()
    con.close()
    return res


def query_fetchone(query_text: str, params=None):
    if params is None:
        params = []
    con = sqlite3.connect('db.sqlite')
    cursor = con.cursor()
    res = cursor.execute(query_text, params).fetchone()
    con.close()
    return res


def query_commit(query_text: str, params=None):
    if params is None:
        params = []
    con = sqlite3.connect('db.sqlite')
    cursor = con.cursor()
    cursor.execute(query_text, params)
    con.commit()
    con.close()


def make_greeting() -> str:
    h = (time.gmtime()[3] + 7) % 24  # Hour in Krasnoyarsk
    if 5 <= h < 12:
        return "Доброе утро"
    elif 12 <= h < 18:
        return "Добрый день"
    elif 18 <= h < 22:
        return "Добрый вечер"
    else:
        return "Доброй ночи"