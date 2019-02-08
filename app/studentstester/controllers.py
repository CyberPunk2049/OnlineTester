from flask import Blueprint, render_template

tester = Blueprint(
    'studentstester',
    __name__,
    url_prefix='/studentstester/'
)

@tester.route('/')
def index():

    values = {
        'title': 'Онлайн тестирование',
        'login_required': False,
        'errors': [],
        'form': None
    }

    return render_template('inprocess.html', values=values)
