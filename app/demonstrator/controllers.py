import datetime
from flask import Blueprint, render_template, request, current_app, redirect, url_for, session
from app.wrappers import login_require
from app.demonstrator.forms import UploadFilesForm
from app.administrator.models import Sessions
from app.demonstrator.models import Theme, Special, Test, Question, Answer
from app.demonstrator.testparse import TestsRtfdom
from app.database import db
import json

demonstrator = Blueprint(
    'demonstrator',
    __name__,
    url_prefix='/demonstrator/'
)


def allowed_file(filename, allowed_extensions):
    # Функция для проверки расширения файла
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


@demonstrator.route('/', methods=['GET', 'POST'])
@login_require
def index():
    test_status = Sessions.query.get(1).test_status
    #TODO Закрыть доступ к другим статусам через адресную строку
    if test_status == 1:
        return redirect(url_for('demonstrator.upload'))
    if test_status == 2:
        return redirect(url_for('demonstrator.test_start'))
    if test_status == 3:
        return redirect(url_for('demonstrator.test_process'))
    if test_status == 4:
        return redirect(url_for('demonstration.test_finish'))


@demonstrator.route('upload/', methods=['GET', 'POST'])
@login_require
def upload():

    values = {
        'title': 'Демонстратор:загрзка',
        'login_required': True,
        'errors': [],
        'form': UploadFilesForm()
    }

    values['form'].theme.choices = [(i.id, i.name) for i in Theme.query.all()]
    values['form'].special.choices = [(i.id, i.name) for i in Special.query.all()]
    error = None
    if values['form'].validate_on_submit():
        variant1 = dict(request.files)['variant1']
        variant2 = dict(request.files)['variant2']

        if not allowed_file(variant1.filename, current_app.config['ALLOWED_EXTENSIONS']):
            values['errors'].append(u'Загружаемые файлы должны иметь расширение .rtf')
            return render_template('demonstrator/upload.html', values=values)

        if not allowed_file(variant2.filename, current_app.config['ALLOWED_EXTENSIONS']):
            values['errors'].append(u'Загружаемые файлы должны иметь расширение .rtf')
            return render_template('demonstrator/upload.html', values=values)
    else:
        for key in values['form'].errors:
            values['errors'].append(values['form'].errors[key])
        return render_template('demonstrator/upload.html', values=values)

    test_theme = Theme.query.get(values['form'].theme.data)
    test_special = Theme.query.get(values['form'].special.data)
    test_num = values['form'].num.data
    test_datetime = datetime.datetime.now()

    for variant in [variant1, variant2]:
        try:
            test_dom_tree = TestsRtfdom()
            test_dom_tree.openString(variant.stream.read().decode().replace('\r', ''))
            test_dom_tree.parse()
            test_dom_tree.add_to_database(test_theme, test_special, test_num, test_datetime)
        except Exception as e:
            print(e)
            values['errors'].append(u"Не удаётся загрузить тесты, не соответствует формат")
            print(values['errors'])

            return render_template('demonstrator/upload.html', values=values)

    if error:
        return render_template('demonstrator/upload.html', values=values)
    sessionparams = Sessions.query.get(1)
    sessionparams.test_status = 2
    session['test_status'] = 2
    db.session.commit()
    return redirect(url_for('demonstrator.index'))


@demonstrator.route('test_start/', methods=['GET', 'POST'])
@login_require
def test_start():

    values = {
        'title': 'Демонстратор: Старт',
        'login_required': True,
        'errors': [],
        'form': None
    }

    variant2 = {
        'id': db.session.query(db.func.max(Test.id)).scalar(),
        'question': []
    }
    variant1 = {
        'id': variant2['id']-1,
        'question': []
    }
    for variant in [variant1, variant2]:
        variant['variant'] = Test.query.get(variant['id']).variant
        for question in Question.query.filter_by(test_id=variant['id']):
            answers = Answer.query.filter_by(question_id=question.id)
            variant['question'].append({
                'name': question.name,
                'text': question.text,
                'answers': [answer.text for answer in answers],
                'answers_bool': [answer.value for answer in answers]
            })

    return json.dumps({
        'variant1': variant1,
        'variant2': variant2
    }, ensure_ascii=False, indent="<br>")


@demonstrator.route('test_process/', methods=['GET', 'POST'])
@login_require
def test_process():

    values = {
        'title': 'Демонстратор: Идёт теститорвание',
        'login_required': True,
        'errors': [],
        'form': None
    }

    return render_template('inprocess.html', values=values)


@demonstrator.route('test_finish/', methods=['GET', 'POST'])
@login_require
def test_finish():

    values = {
        'title': 'Демонстратор:тестирование окончено',
        'login_required': False,
        'errors': [],
        'form': None
    }

    return render_template('inprocess.html', values=values)
