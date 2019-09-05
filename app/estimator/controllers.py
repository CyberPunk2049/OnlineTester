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


@estimator.route('tests_list/')
@login_require
def tests_list():
    """
    Возвращает страницу со списком пройденных тестов
    """

    values = {
        'title': 'Результаты тестов',
        'login_required': True,
        'errors': [],
        'form': None
    }

    pass


@estimator.route('test_result/')
@login_require
def test_result():
    """
    Возвращает страницу со результатами теста
    """
    pass


@estimator.route('student_answer/')
@login_require
def student_answer():
    """
    Возвращает страницу с ответами студента на тест
    """
    pass