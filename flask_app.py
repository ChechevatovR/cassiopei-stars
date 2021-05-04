# -*- coding: utf-8 -*-

from authorizer import check_user_auth
from shared import *
import authorizer
import scoreboard
import manual
import messages
import tasks_list
import task_displayer
from tasks_functions import *
from flask import Flask, redirect, send_from_directory, g

app = Flask(__name__)
app.register_blueprint(authorizer.bp)
app.register_blueprint(scoreboard.bp)
app.register_blueprint(manual.bp)
app.register_blueprint(messages.bp)
app.register_blueprint(tasks_list.bp)
app.register_blueprint(task_displayer.bp)


with app.app_context():
    app.config['tasks'] = {id[0]: Task(id[0]) for id in query_fetchall('SELECT id FROM tasks WHERE is_public = 1', open_connection=True)}
    app.config['tasks'][1].generator = task1_generator
    app.config['tasks'][2].generator = task2_generator
    app.config['tasks'][4].generator = task4_generator
    app.config['tasks'][6].generator = task6_generator
    app.config['tasks'][9].generator = task9_generator
    app.config['tasks'][14].generator = task14_generator
    app.config['tasks'][15].checker = task15_checker
    app.config['tasks'][21].checker = task21_checker
    app.config['tasks'][23].generator = task23_generator
    app.config['tasks'][29].generator = task29_generator
    app.config['tasks'][43].generator = task43_generator



@app.route('/')
def root():
    if not (user := check_user_auth()).is_authorized:
        return redirect('/auth')
    return redirect('/tasks')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('/static', 'favicon.ico')


@app.route('/task-static-content/<path>')
def serve_static_payload(path: str):
    return send_from_directory('task-static-content', path, cache_timeout=0)


@app.route('/task-generated-content/<path1>/<path2>')
def serve_generated_payload(path1, path2):
    return send_from_directory('task-generated-content', f'{path1}/{path2}', cache_timeout=0)


@app.before_request
def connect_db():
    g.db_con = sqlite3.connect('db.sqlite')
    g.db_cur = g.db_con.cursor()


@app.after_request
def disconnect_db(response):
    g.db_con.close()
    return response


if __name__ == '__main__':
    app.run(host='localhost', port=80, debug=True)

# TODO Условие и названия 45 таски ждут модерации