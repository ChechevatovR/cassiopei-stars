from shared_core import *
from team import Team
from flask import request


class Task:
    id: int

    type_question: str
    # static
    # generated

    type_answer: str
    # static
    # generated
    # validated

    generator = None
    checker = None

    def __init__(self, id: int):
        self.id = id
        self.type_question = query_fetchone('SELECT type_question FROM tasks WHERE id = ?', [self.id])[0]
        self.type_answer = query_fetchone('SELECT type_answer FROM tasks WHERE id = ?', [self.id])[0]

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

    def attachments(self, team=Team(-1)):
        if self.type_question == 'static':
            return query_fetchone('SELECT payload FROM tasks WHERE id = ?', [self.id])
        elif self.type_question == 'generated':
            if self.type_answer == 'generated':
                payload, answer = self.generator(team.id)
            else:
                payload = self.generator(team.id)

    def check(self):
        if self.attempts_required > 0:
            # Multisolve
            return self.generate_payload()
        else:
            # One attempt - correct answer is in database
            answer_got = None

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
