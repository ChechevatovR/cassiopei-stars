from flask import current_app, request


def task15_checker():
    answer = request.form.get('answer')
    if answer is not None:  # Ответ нужно отправлять не через форму
        return False
    return True


with current_app.app_context():
    current_app.config['tasks'][15].checker = task15_checker
