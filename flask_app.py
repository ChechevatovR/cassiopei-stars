# -*- coding: utf-8 -*-

from authorizer import check_user_auth
from shared import *
import authorizer
import scoreboard
import manual
import messages
import tasks_list
import task_displayer
import admin
# import poll_
from tasks_functions import *
from flask import Flask, redirect, send_from_directory, g

app = Flask(__name__)
app.register_blueprint(authorizer.bp)
app.register_blueprint(scoreboard.bp)
app.register_blueprint(manual.bp)
app.register_blueprint(messages.bp)
app.register_blueprint(tasks_list.bp)
app.register_blueprint(task_displayer.bp)
app.register_blueprint(admin.bp)
# app.register_blueprint(poll.bp)


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


@app.before_request
def find_tasks():
    with app.app_context():
        app.config['tasks'] = {id_[0]: Task(id_[0]) for id_ in
                               query_fetchall('SELECT id FROM tasks WHERE is_public = 1', open_connection=True)}
        if app.config['tasks'].get(1, False):
            app.config['tasks'][1].generator = task1_generator

        if app.config['tasks'].get(2, False):
            app.config['tasks'][2].generator = task2_generator

        if app.config['tasks'].get(4, False):
            app.config['tasks'][4].generator = task4_generator

        if app.config['tasks'].get(6, False):
            app.config['tasks'][6].generator = task6_generator

        if app.config['tasks'].get(9, False):
            app.config['tasks'][9].generator = task9_generator

        if app.config['tasks'].get(14, False):
            app.config['tasks'][14].generator = task14_generator

        if app.config['tasks'].get(15, False):
            app.config['tasks'][15].checker = task15_checker

        if app.config['tasks'].get(21, False):
            app.config['tasks'][21].checker = task21_checker

        if app.config['tasks'].get(23, False):
            app.config['tasks'][23].generator = task23_generator

        if app.config['tasks'].get(27, False):
            app.config['tasks'][27].generator = task27_generator

        if app.config['tasks'].get(29, False):
            app.config['tasks'][29].generator = task29_generator

        if app.config['tasks'].get(43, False):
            app.config['tasks'][43].generator = task43_generator

        if app.config['tasks'].get(46, False):
            app.config['tasks'][46].checker = task46_checker


@app.after_request
def disconnect_db(response):
    g.db_con.close()
    return response


if __name__ == '__main__':
    app.run(host='localhost', port=80, debug=True)
