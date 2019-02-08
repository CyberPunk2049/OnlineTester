from flask import Blueprint, render_template
from app.wrappers import login_require


estimator = Blueprint(
    'estimator',
    __name__,
    url_prefix='/estimator/'
)


@estimator.route('/')
@login_require
def index():

    values = {
        'title': 'Результаты тестов',
        'login_required': True,
        'errors': [],
        'form': None
    }

    return render_template('inprocess.html', values=values)
