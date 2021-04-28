# -*- coding: utf-8 -*-

from shared import *
from authorizer import check_user_auth
from flask import Blueprint, redirect, url_for, render_template, make_response, current_app, send_file

bp = Blueprint('tasks_list', __name__, template_folder='templates')


@bp.route('/tasks')
def tasks_list():
    user = check_user_auth()
    if not user.is_authorized:
        return redirect('/auth')
    # print(user.id, user.is_authorized)

    with current_app.app_context():
        tasks = current_app.config['tasks']

    return render_template(
        'tasks.html',
        tasks=[dict(zip(['id', 'title', 'subtitle', 'solved_by_n', 'cur_score'], [task.id, task.title_full, task.subtitle, task.solved_by_n, task.score])) for task in tasks.values()],
        header=make_header('Список заданий', user=user, exclude_home=True))





