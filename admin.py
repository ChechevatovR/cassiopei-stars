from shared import *
from authorizer import check_user_auth
from flask import Blueprint, request, redirect, url_for, render_template, make_response


bp = Blueprint('admin', __name__, template_folder='templates')


@bp.route('/9ce04b60783e43d0c3c5edd291718cc2635cbadc5922c368ee7d1fab6f4b6b46', methods=['GET'])
def admin():
    if not (user := check_user_auth()).is_authorized or user.team.name != 'Жюри':
        return '403 Unauthorized', 403

    teams = [dict(zip(['id', 'name'], i)) for i in query_fetchall('SELECT id, name FROM teams')]
    solutions = query_fetchall('select team_id, task_id from solutions')
    print(solutions)
    solutions_messages = [f"\"{query_fetchone('select title from tasks where id=?',[solutions[-1][1]])[0]}\" от \"{query_fetchone('select name from teams where id=?',[solutions[-1][0]])[0]}\"",
                          f"\"{query_fetchone('select title from tasks where id=?',[solutions[-2][1]])[0]}\" от \"{query_fetchone('select name from teams where id=?',[solutions[-2][0]])[0]}\"",
                          f"\"{query_fetchone('select title from tasks where id=?',[solutions[-3][1]])[0]}\" от \"{query_fetchone('select name from teams where id=?',[solutions[-3][0]])[0]}\"",
                          f"\"{query_fetchone('select title from tasks where id=?',[solutions[-4][1]])[0]}\" от \"{query_fetchone('select name from teams where id=?',[solutions[-4][0]])[0]}\""]
    print(solutions_messages)
    return render_template(
        'admin.html',
        header=make_header('Админка', user),
        authorized=True,
        team_id=user.team.id,
        teams=teams,
        last_solution_message=solutions_messages
    )


@bp.route('/9ce04b60783e43d0c3c5edd291718cc2635cbadc5922c368ee7d1fab6f4b6b46/fetch', methods=['POST'])
def admin_fetch():
    if not (user := check_user_auth()).is_authorized or user.team.name != 'Жюри':
        return '403 Unauthorized', 403
    if (query := request.form.get('query', '')) == '':
        return '400 Bad request', 400

    result = query_fetchall(query)

    print(*result, sep='\n')

    if request.form.get('HTML', '') != '':
        html = ''
        for row in result:
            row_str = ''
            for item in row:
                row_str += f'<td>{item}</td>'
            html += f'<tr>{row_str}</tr>'
        return '<style>table, th, td {  border: 1px solid black;  border-collapse: collapse;}</style>' +  f'<table>{html}</table>'

    if request.form.get('CSV', '') != '':
        csv = ''
        for row in result:
            row_str = ''
            for item in row:
                row_str += str(item) + ','
            csv += row_str[:-1] + '<br>'  # kinda strange line break
        return csv


@bp.route('/9ce04b60783e43d0c3c5edd291718cc2635cbadc5922c368ee7d1fab6f4b6b46/commit', methods=['POST'])
def admin_commit():
    if not (user := check_user_auth()).is_authorized or user.team.name != 'Жюри':
        return '403 Unauthorized', 403

    if (query := request.form.get('query', '')) == '':
        return '400 Bad request', 400

    query_commit(query)
    return 'Вроде ОК, но я не проверял'
