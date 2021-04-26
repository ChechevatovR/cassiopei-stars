from shared_core import *
from team import Team


class User:
    id: int
    is_authorized: bool

    def __init__(self, id: int, is_authorized: bool):
        self.id = id
        self.is_authorized = is_authorized

    @property
    def login(self):
        return query_fetchone('SELECT login FROM users WHERE id = ?', [self.id])[0]

    @property
    def team(self):
        return Team(query_fetchone('SELECT team_id FROM users WHERE id = ?', [self.id])[0])

    @property
    def name1(self):
        return query_fetchone('SELECT name FROM users WHERE id = ?', [self.id])[0]

    @property
    def name2(self):
        return query_fetchone('SELECT lastname FROM users WHERE id = ?', [self.id])[0]
