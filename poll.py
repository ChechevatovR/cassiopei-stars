from shared import *
from flask import Blueprint, request, redirect, url_for, render_template, make_response, current_app
import sqlite3

bp = Blueprint('poll', __name__, template_folder='templates')


@bp.route('/poll')
def main():
    if not (user := check_user_auth()).is_authorized:
        return redirect('/auth')
    if user.id > 46:
        return redirect('/tasks')
    header = make_header('Опрос', user)
    return render_template('poll.html', header = header, answers = check_answers(user))


@bp.route('/poll', methods = ['post'])
def get_answers():
    if not (user := check_user_auth()).is_authorized:
        return redirect('/auth')
    if check_answers(user):
        return redirect('/poll')
    if user.id > 46:
        return redirect('/tasks')
    favorite_task = request.form.get('favorite_task')
    worst_task = request.form.get('worst_task')
    site_comment = request.form.get('site_comment')
    theme = request.form.get('which')
    reg_reason = request.form.get('why')
    new_knowledge = request.form.get('what')
    difficulty = request.form.get('difficulty')
    comment = request.form.get('comment')

    query_commit('INSERT INTO poll_results VALUES (?, ?, ?, ?, ?, ? ,?, ?, ?)',
                 [user.id, favorite_task, worst_task, site_comment, theme,
                  reg_reason, new_knowledge, difficulty, comment])

    return redirect('/poll')