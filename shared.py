# -*- coding: utf-8 -*-

from shared_core import *
from user import User
from team import Team
import time
import sqlite3
from flask import render_template, request


def check_user_auth() -> User:
    login = request.cookies.get('login')
    token = request.cookies.get('token')
    if login is None or token is None:
        return User(-1, False)
    user_id = query_fetchone('SELECT id FROM users WHERE login = ?', [login])[0]
    query_commit("DELETE FROM tokens WHERE expires_on <= datetime('now')")
    result = query_fetchone('SELECT COUNT(*) FROM tokens WHERE user_id = ? AND token = ?', [user_id, token])[0]
    return User(user_id, result > 0)


def make_header(page_name: str, user=User(-1, False), **params) -> str:
    if user.is_authorized:
        return render_template(
            '_header.html',
            authorized=True,
            page_name=page_name,
            **header_data(user),
            **params)
    else:
        return render_template(
            '_header.html',
            authorized=False,
            page_name=page_name,
            **params
        )


def header_data(user: User) -> dict:
    return {
        'greeting': make_greeting(),
        'user_name': user.name1,
        'team_name': user.team.name,
        'team_score': user.team.score,
        'team_tasks': user.team.tasks
    }


def task_header_data(team_id: int, task_id: int) -> dict:
    solved = query_fetchone('SELECT COUNT(*) FROM solutions WHERE task_id = ? AND team_id = ?', [task_id, team_id])[0]
    cur_score = 0
    if solved:
        cur_score = SCORE_PER_TASK // query_fetchone('SELECT COUNT(*) FROM solutions WHERE task_id = ?', [task_id])[0]
    solved_by_teams = query_fetchone('SELECT COUNT(*) FROM solutions WHERE task_id = ?', [task_id])[0]
    multisolve = query_fetchone('SELECT attempts_required FROM tasks WHERE id = ?', [task_id])[0] > 0
    correct_in_row = 0
    try:
        correct_in_row = query_fetchone('SELECT in_row FROM task_status WHERE task_id = ? AND team_id = ?', [task_id, team_id])[0]
    except TypeError:
        pass
    res = {
        'solved': solved,
        'cur_score': cur_score,
        'solved_by_teams': solved_by_teams,
        'multisolve': multisolve,
        'correct_in_row': correct_in_row
    }
    return res


def refresh_task_solution(team_id: int, task_id: int) -> None:
    in_row = query_fetchone('SELECT in_row FROM task_status WHERE task_id = ? AND team_id = ?', [task_id, team_id])[0]
    required = query_fetchone('SELECT attempts_required FROM tasks WHERE id = ?', [task_id])[0]
    # print(in_row, required)
    if in_row == required:
        query_commit('REPLACE INTO solutions (team_id, task_id) VALUES (?, ?)', [team_id, task_id])