# -*- coding: utf-8 -*-

from shared import *
from authorizer import check_user_auth
from flask import Blueprint, redirect, url_for, render_template, make_response, current_app, send_file

bp = Blueprint('tasks', __name__, template_folder='templates')


@bp.route('/tasks/task<task_id>', methods=['GET'])
def task_get(task_id: int):
    if not (user := check_user_auth()).is_authorized:
        return redirect('/auth')
    task_id = int(task_id)
    with current_app.app_context():
        tasks = current_app.config['tasks']

    try:
        task = tasks[task_id]
    except KeyError:
        return '404 Not found', 404

    query_commit('INSERT OR IGNORE INTO task_status (team_id, task_id) VALUES (?, ?)', [user.team.id, task.id])
    query_commit('UPDATE task_status SET in_row = 0 WHERE task_id = ? AND team_id = ? AND status = 1', [task.id, user.team.id])
    query_commit('UPDATE task_status SET status = 1, required_answer = null WHERE task_id = ? AND team_id = ?', [task.id, user.team.id])

    if task.type_question == 'generated':
        if task.type_answer == 'generated':
            payload, answer = task.generator(user.team.id)
            query_commit('UPDATE task_status SET required_answer = ? WHERE task_id = ? AND team_id = ?', [answer, task.id, user.team.id])
        elif task.type_answer == 'validated':
            payload = task.generator(user.team.id)
    elif task.type_question == 'static':
        payload = query_fetchone('SELECT payload FROM tasks WHERE id = ?', [task.id])[0]

    # print(payload)

    return render_template(
        'task.html',
        header=make_header(task.title_full, user),
        task={
            'emoji': task.emoji,
            'title': task.title,
            'title_full': task.title_full,
            'subtitle': task.subtitle,
            'description': task.description,
            'score': task.score * task.is_solved_by(user.team),
            'solved_by_n': task.solved_by_n,
            'multisolve': task.attempts_required > 1,
            'attempts_required': task.attempts_required,
            'correct_in_row': task.correct_in_row(user.team),
            'input_form': task.input_form,
            'attachments': payload
        },
    )


@bp.route('/tasks/task<task_id>', methods=['POST'])
def task_post(task_id: int):
    if not (user := check_user_auth()).is_authorized:
        return redirect('/auth')
    task_id = int(task_id)
    with current_app.app_context():
        tasks = current_app.config['tasks']

    task = tasks[task_id]
    if task.type_answer == 'static':
        answer = request.form.get('answer')
        required = query_fetchone('SELECT answer FROM tasks WHERE id = ?', [task.id])[0]
        correct = answer.strip() == required.strip()
    elif task.type_answer == 'generated':
        answer = request.form.get('answer')
        required = query_fetchone('SELECT required_answer FROM task_status WHERE task_id = ? AND team_id = ?', [task.id, user.team.id])[0]
        correct = answer.strip() == required.strip()
        # print(answer, required, correct)
    elif task.type_answer == 'validated':
        correct = task.checker(user.team.id)
    else:
        raise ValueError

    # print(query_fetchone('SELECT in_row FROM task_status WHERE team_id = ? AND task_id = ?', [user.team.id, task.id]))
    query_commit('UPDATE task_status SET in_row = 0 WHERE task_id = ? AND team_id = ? AND status = 0', [task.id, user.team.id])

    if correct:
        query_commit('UPDATE task_status SET status = 0, in_row = in_row + 1 WHERE team_id = ? AND task_id = ?', [user.team.id, task.id])
        refresh_task_solution(user.team.id, task.id)
    else:
        query_commit('UPDATE task_status SET status = 0, in_row = 0 WHERE team_id = ? AND task_id = ?', [user.team.id, task.id])
    return redirect(f'/tasks/task{task_id}')