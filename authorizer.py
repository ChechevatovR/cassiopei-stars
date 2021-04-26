# -*- coding: utf-8 -*-
from shared import *
from flask import Blueprint, request, session, redirect, url_for, render_template, make_response
from datetime import timedelta, datetime
from hashlib import sha256
from user import User
import sqlite3
import secrets
import flask

bp = Blueprint('authorizer', __name__, template_folder='templates')


@bp.route('/auth', methods=['GET'])
def auth_get():
    response = make_response(render_template('auth.html'))
    response.set_cookie('token', 'zzz')
    return response


@bp.route('/auth', methods=['POST'])
def auth_post():
    login = str(request.form.get('login'))[:420]
    password = str(request.form.get('password'))[:420]
    if login is not None or login == '':
        if password is None or password == '':
            return '400 Bad Request', 400
        # Проверим совпадение пары логин-пароль
        user_exists = query_fetchone('SELECT COUNT(*) FROM users WHERE login = ? AND password_hash = ?', [login, sha256(password.encode('utf-8')).hexdigest()])[0]
        if user_exists == 0:
            return render_template('auth.html', error='Пользователь с таким логином и паролем не найден')

        user_id = query_fetchone('SELECT id FROM users WHERE login = ?', [login])[0]
        response = make_response(redirect('/tasks'))
        return _add_token_cookies_to_response(response, user_id)

    # Логин не предоставлен
    return '400 Bad Request', 400


@bp.route('/reg', methods=['GET'])
def reg_get(**kwargs):
    team = request.args.get('team')
    if team is None:
        return '400 Bad request', 400
    else:
        team_name = query_fetchone('SELECT name FROM teams WHERE id = ?', [int(team)])[0]
        return render_template('register.html', team_name=team_name, team_id=team, **kwargs)


@bp.route('/reg', methods=['POST'])
def reg_post():
    login = str(request.form.get('login'))[:420]
    password = str(request.form.get('password'))[:420]
    name = str(request.form.get('name'))[:420]
    lastname = str(request.form.get('name'))[:420]
    team_id = request.args.get('team')

    if team_id is None or login is None or login == '' or password is None or password == '' or name is None or name == '' or lastname is None or lastname == '':
        return '400 Bad request', 400

    team_users = query_fetchall('SELECT login FROM users WHERE team_id = ?', [team_id])
    if len(team_users) >= 3:
        return reg_get(error='Эта команда уже заполнена')

    try:
        query_commit('INSERT INTO users (login, password_hash, name, lastname, team_id) VALUES (?, ?, ?, ?, ?)', [login, sha256(password.encode('utf-8')).hexdigest(), name, lastname, team_id])
        user_id = query_fetchone('SELECT id FROM users WHERE login = ?', [login])[0]
        response = make_response(redirect('/tasks'))
        return _add_token_cookies_to_response(response, user_id)
    except sqlite3.IntegrityError as e:
        print(e)
        return reg_get(error='Этот логин уже занят')


@bp.route('/reg-team', methods=['GET'])
def reg_team_get():
    return render_template('register-team.html')


@bp.route('/reg-team', methods=['POST'])
def reg_team_post():
    name = str(request.form.get('team-name'))[:420]
    if name is not None and name != '':
        try:
            query_commit('INSERT INTO teams (name) VALUES (?)', [name])
            result = query_fetchall('SELECT id FROM teams WHERE name = ?', [name])
            register_url = url_for('authorizer.reg_get', team=result[0][0])
            return redirect(register_url)
        except sqlite3.IntegrityError as er:
            if er.args[0] == 'UNIQUE constraint failed: teams.name':
                return render_template('register-team.html', error='Команда уже зарегистрирована')
            if er.args[0] == 'NOT NULL constraint failed: teams.name':
                return '400 Bad request', 400
            print(er.args)
    return '400 Bad request', 400


def _add_token_cookies_to_response(response: flask.Response, user_id: int) -> flask.Response:
    token = secrets.token_hex(32)
    login = query_fetchone('SELECT login FROM users WHERE id = ?', [user_id])[0]
    query_commit("REPLACE INTO tokens(user_id, token, expires_on) VALUES (?, ?, datetime('now', '+12 hours'))", [user_id, token])
    response.set_cookie('login', login, expires=datetime.now() + timedelta(hours=12))
    response.set_cookie('token', token, expires=datetime.now() + timedelta(hours=12))
    return response
