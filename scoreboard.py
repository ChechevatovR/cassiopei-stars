from shared import *
from flask import Blueprint, request, redirect, url_for, render_template, make_response
import sqlite3

bp = Blueprint('scoreboard', __name__, template_folder='templates')


@bp.route('/scoreboard', methods=['GET'])
def scoreboard_get():

    table_dict = _get_scoreboard_dict()
    table_header = ['', 'Команда', 'Балл'] + [i for i in query_fetchall('SELECT id, title FROM tasks WHERE is_public = 1')]
    table_data = []
    for key, value in table_dict.items():
        table_data += [[0] + [key] + value]
    table_data.sort(key=lambda val: val[2], reverse=True)
    _calc_positions(table_data)

    header = make_header('Рейтинг', exclude_rating=True)
    if (user := check_user_auth()).is_authorized:
        header = make_header('Рейтинг', user=user, exclude_rating=True)

    return render_template(
        'scoreboard.html',
        table1_header=table_header[:3],
        table1_data=[dict(zip(['position', 'name', 'score'], i[:3])) for i in table_data],
        table2_header=[dict(zip(['id', 'full', 'short'], [i[0], i[1], i[1].split()[0]])) for i in table_header[3:]],
        table2_data=[i[3:] for i in table_data],
        header=header
    )


def _calc_positions(table_data: list):
    prev_score = table_data[0][2]
    sequences = [[0, 0]]
    for i in range(1, len(table_data)):
        cur_score = table_data[i][2]
        # print(i, cur_score, prev_score)
        if cur_score == prev_score:
            sequences[-1][1] += 1
        else:
            sequences += [[i, i]]
        prev_score = cur_score
    # print(sequences)
    for seq in sequences:
        if seq[0] == seq[1]:
            table_data[seq[0]][0] = f'{seq[0] + 1}'
        else:
            for i in range(seq[0], seq[1] + 1):
                table_data[i][0] = f'{seq[0] + 1}-{seq[1] + 1}'


def _get_scoreboard_dict():
    task_ids = [i[0] for i in query_fetchall('SELECT id FROM tasks WHERE is_public = 1')]
    table_dict = dict.fromkeys([i[0] for i in query_fetchall('SELECT name FROM teams')])
    for key in table_dict.keys():
        table_dict[key] = [0] * (len(task_ids) + 1)
    for ind, task_id in enumerate(task_ids):
        solved_by = query_fetchone('SELECT COUNT(*) FROM solutions WHERE task_id = ?', [task_id])[0]
        if solved_by == 0:
            continue
        score_per_solution = SCORE_PER_TASK // (solved_by)
        for team_name in [i[0] for i in query_fetchall(
                'SELECT name FROM teams WHERE id IN (SELECT team_id FROM solutions WHERE task_id = ?)', [task_id])]:
            table_dict[team_name][0] += score_per_solution
            table_dict[team_name][ind + 1] = score_per_solution
    return table_dict
