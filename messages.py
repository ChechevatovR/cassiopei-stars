from shared import *
from flask import Blueprint, request, redirect, url_for, render_template, make_response

bp = Blueprint('news', __name__, template_folder='templates')


@bp.route('/messages', methods=['GET'])
def news_get():
    if not (user := check_user_auth()).is_authorized:
        return redirect('/auth')

    messages = [dict(zip(['date', 'from', 'to', 'message'], i)) for i in query_fetchall(
        '''SELECT date, src, dst, text FROM messages WHERE src = ? OR dst = ? OR dst = 0''',
        [user.team.id, user.team.id]
    )]

    for message in messages:
        if message['to'] == 0:
            message['to'] = 'Всем'
        else:
            message['to'] = query_fetchone('SELECT name FROM teams WHERE id = ?', [message['to']])[0]
        message['from'] = query_fetchone('SELECT name FROM teams WHERE id = ?', [message['from']])[0]
    return render_template(
        'messages.html',
        messages=messages,
        header=make_header(
            'Сообщения',
            user,
            exclude_messages=True
        )
    )


@bp.route('/messages', methods=['POST'])
def news_post():
    if not (user := check_user_auth()).is_authorized:
        return redirect('/auth')

    message = request.form.get('question')
    query_commit(
        "INSERT INTO messages (date, src, dst, text) VALUES (CURRENT_TIMESTAMP, ?, 1, ?)",
        [user.team.id, message]
    )
    return redirect('/messages')
