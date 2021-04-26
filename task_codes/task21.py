from flask import current_app, request


def task21_checker():
    answer = request.form.get('answer')
    if answer is not None:  # Ответ нужно отправлять не через форму
        return False
    return 'tea' in [i.lower() for i in request.cookies.keys()]


with current_app.app_context():
    current_app.config['tasks'][21].checher = task21_checker
