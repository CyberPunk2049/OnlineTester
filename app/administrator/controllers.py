from flask import Blueprint, redirect, url_for, render_template, request, session
from app.administrator.forms import LoginForm
from app.administrator.models import Subject, User, Sessions
from app.database import db
from app.wrappers import login_require

administrator = Blueprint(
    'administrator',
    __name__,
    url_prefix='/administrator/'
)


@administrator.route('/')
@login_require
def index():

    values = {
        'title': 'Авторизация',
        'login_required': True,
        'errors': [],
        'form': None
    }

    return render_template('administrator/index.html', values=values)


@administrator.route('login/', methods=['GET', 'POST'])
def login():

    values = {
        'title': 'Авторизация',
        'login_required': False,
        'errors': [],
        'form': LoginForm()
    }

    values['form'].subject.choices = [(i.id, i.name) for i in Subject.query.all()]

    if request.method == 'GET' and 'id' in session:
        return redirect(url_for('administrator.index'))

    if values['form'].validate_on_submit():
    #TODO Разобраться с логином и паролем при повторном входе
        if User.query.filter_by(username=values['form'].username.data, password=values['form'].password.data).all():
            sessionparams = Sessions.query.get(1)
            sessionparams.subject = values['form'].subject.data
            session['id'] = sessionparams.session_id
            session['subject'] = sessionparams.subject
            session['subject_name'] = Subject.query.get(sessionparams.subject).name
            session['test_status'] = sessionparams.test_status
            session['quest_num'] = sessionparams.quest_num
            db.session.commit()
            return redirect(url_for('administrator.index'))
        else:
            values['errors'].append(u'Введён неверный логин или пароль')
            return render_template('administrator/login.html', values=values)
    return render_template('administrator/login.html', values=values)


@administrator.route('logout/')
@login_require
def logout():
    del session['id']
    return redirect(url_for('administrator.login'))


