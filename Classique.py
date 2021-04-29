from shared_core import *


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


class Team:
    id: int

    def __init__(self, id: int):
        self.id = id

    @property
    def is_real_team(self):
        return query_fetchone('SELECT COUNT(*) FROM teams WHERE id = ?', [self.id])[0] > 0

    @property
    def name(self):
        return query_fetchone('SELECT name FROM teams WHERE id = ?', [self.id])[0]

    @property
    def score(self):
        score = 0
        for task_id in [i[0] for i in query_fetchall('SELECT task_id FROM solutions WHERE team_id = ?', [self.id])]:
            score += Task(task_id).score
        return score

    @property
    def tasks(self):
        return query_fetchone('SELECT COUNT(*) FROM solutions WHERE team_id = ?', [self.id])[0]

    @property
    def invite(self):
        return int(query_fetchone('SELECT invite FROM teams WHERE id = ?', [self.id])[0])

    @property
    def size(self):
        return query_fetchone('SELECT COUNT(*) FROM users WHERE team_id = ?', [self.id])[0]


class Task:
    id: int
    generator = None
    checker = None

    def __init__(self, id: int):
        self.id = id

    @property
    def type_question(self):
        return query_fetchone('SELECT type_question FROM tasks WHERE id = ?', [self.id])[0]

    @property
    def type_answer(self):
        return query_fetchone('SELECT type_answer FROM tasks WHERE id = ?', [self.id])[0]

    @property
    def solved_by_n(self):
        return query_fetchone('SELECT COUNT(*) FROM solutions WHERE task_id = ?', [self.id])[0]

    @property
    def score(self):
        if self.solved_by_n == 0:
            return 0
        return SCORE_PER_TASK // self.solved_by_n

    def is_solved_by(self, team: Team):
        return query_fetchone('SELECT COUNT(*) FROM solutions WHERE task_id = ? AND team_id = ?', [self.id, team.id])[0] > 0

    @property
    def attempts_required(self):
        return query_fetchone('SELECT attempts_required FROM tasks WHERE id = ?', [self.id])[0]

    def correct_in_row(self, team: Team):
        try:
            return query_fetchone('SELECT in_row FROM task_status WHERE task_id = ? AND team_id = ?', [self.id, team.id])[0]
        except TypeError:
            return 0

    @property
    def emoji(self):
        return query_fetchone('SELECT title FROM tasks WHERE id = ?', [self.id])[0].split()[0]

    @property
    def title(self):
        return ' '.join(query_fetchone('SELECT title FROM tasks WHERE id = ?', [self.id])[0].split()[1:])

    @property
    def title_full(self):
        return query_fetchone('SELECT title FROM tasks WHERE id = ?', [self.id])[0]

    @property
    def subtitle(self):
        return query_fetchone('SELECT subtitle FROM tasks WHERE id = ?', [self.id])[0]

    @property
    def description(self):
        return query_fetchone('SELECT description FROM tasks WHERE id = ?', [self.id])[0]

    @property
    def input_form(self):
        return query_fetchone('SELECT input_form FROM tasks WHERE id = ?', [self.id])[0]

    @property
    def attachments(self):
        if self.type_question == 'static':
            return query_fetchone('SELECT payload FROM tasks WHERE id = ?', [self.id])[0]
