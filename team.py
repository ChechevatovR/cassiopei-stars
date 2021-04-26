from shared_core import *


class Team:
    id: int

    def __init__(self, id: int):
        self.id = id

    @property
    def name(self):
        return query_fetchone('SELECT name FROM teams WHERE id = ?', [self.id])[0]

    @property
    def score(self):
        from task import Task
        score = 0
        for task_id in [i[0] for i in query_fetchall('SELECT task_id FROM solutions WHERE team_id = ?', [self.id])]:
            score += Task(task_id).score
        return score

    @property
    def tasks(self):
        return query_fetchone('SELECT COUNT(*) FROM solutions WHERE team_id = ?', [self.id])[0]
