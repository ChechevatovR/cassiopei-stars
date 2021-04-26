from shared import *
from authorizer import check_user_auth
from flask import Blueprint, request, redirect, url_for, render_template, make_response
import flask

bp = Blueprint('manual', __name__, template_folder='templates')


@bp.route('/manual')
def manual():
    if not (user := check_user_auth()).is_authorized:
        return render_template(
            'manual.html',
            header=make_header('Помощь', user, exclude_manual=True),
            authorized=True,
            team_id=user.team.id
        )
    return render_template(
        'manual.html',
        header=make_header('Помощь', exclude_manual=True),
        authorized=False
    )
