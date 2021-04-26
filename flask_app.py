# -*- coding: utf-8 -*-
from werkzeug import run_simple

from authorizer import check_user_auth
from shared_core import query_fetchall
import authorizer
import scoreboard
import manual
import messages
import tasks
from task import Task
from flask import Flask, redirect, send_from_directory


app = Flask(__name__)
app.register_blueprint(authorizer.bp)
app.register_blueprint(scoreboard.bp)
app.register_blueprint(manual.bp)
app.register_blueprint(messages.bp)
app.register_blueprint(tasks.bp)

app.config['PROFILE'] = True


with app.app_context():
    app.config['tasks'] = {id[0]: Task(id[0]) for id in query_fetchall('SELECT id FROM tasks WHERE is_public = 1', [])}
    for task_id in app.config['tasks'].keys():
        eval(f'__import__("task_codes.task{task_id}")')


@app.route('/')
def root():
    if not (user := check_user_auth()).is_authorized:
        return redirect('/auth')
    return redirect('/tasks')


@app.route('/favicon.ico')
def favicon():
    print('Got a favicon request')
    return send_from_directory('/static', 'favicon.ico')


if __name__ == '__main__':
    app.run(host='localhost', port=80, debug=True)
