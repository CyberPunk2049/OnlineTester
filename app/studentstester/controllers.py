import json
from flask import Blueprint, render_template, session, request, redirect, url_for
from app.database import db
from app.administrator.models import Sessions
from app.demonstrator.models import Test, Question, Answer
from app.studentstester.models import Student, StudentAnswer
from app.studentstester.forms import PersonalDataForm

studentstester = Blueprint(
    'studentstester',
    __name__,
    url_prefix='/studentstester/'
)


@studentstester.route('/')
def index():
    test_status = Sessions.query.get(1).test_status
    if test_status == 1 or test_status == 2:
        return redirect(url_for('studentstester.no_test'))
    if test_status == 3:
        return redirect(url_for('studentstester.personal_data'))
    if test_status == 4:
        return redirect(url_for('studentstester.test_process'))
    if test_status == 5:
        return redirect(url_for('studentstester.test_end'))


@studentstester.route('no_test/')
def no_test():
    """
    При отсутствии загруженных тестов возвращает страницу ожидания
    """
    # Проверка и перенаправление запроса в случае если он не соответствует состоянию тестирования
    if request.method == 'GET':
        actual_controller = check_status()
        if 'location' in request.values.to_dict().keys():
            return need_reload(actual_controller, 'studentstester.no_test')

        if actual_controller != 'studentstester.no_test':
            return redirect(url_for(actual_controller))

    values = {
        'title': 'Онлайн тестирование',
        'page_info': 'Ожидайте начала тестирования',
        'login_required': False,
        'errors': [],
        'form': None
    }
    return render_template('studentstester/notest.html', values=values)


@studentstester.route('personal_data/', methods=['GET', 'POST', 'AJAX'])
def personal_data():
    """
    Возвращает форму ввода персоональных данных
    """

    # Проверка и перенаправление запроса в случае если он не соответствует состоянию тестирования
    if request.method == 'GET':
        actual_controller = check_status()
        if 'location' in request.values.to_dict().keys():
            return need_reload(actual_controller, 'studentstester.personal_data')

        if actual_controller != 'studentstester.personal_data':
            return redirect(url_for(actual_controller))

    values = {
        'title': 'Онлайн тестирование',
        'page_info': 'Зарегистрируйтесь на тестирование',
        'login_required': False,
        'errors': [],
        'form': PersonalDataForm()
    }
    if values['form'].validate_on_submit():
        student = Student(
            name=values['form'].name.data,
            surname=values['form'].surname.data,
            patronymic=values['form'].patronymic.data,
            student_id=values['form'].student_id.data,
            group=values['form'].group.data,
            email=values['form'].email.data,
        )
        db.session.add(student)
        db.session.commit()
        session['student_id'] = student.id
        return redirect(url_for('studentstester.choice_of_variant'))

    else:
        for key in values['form'].errors:
            values['errors'].append(values['form'].errors[key])
    return render_template('studentstester/personaldata.html', values=values)


@studentstester.route('choice_of_variant/', methods=['GET', 'PUT'])
def choice_of_variant():
    """
    Возвращает страницу выбора варианта
    """
    values = {
        'title': 'Онлайн тестирование',
        'page_info': 'Выберите вариант',
        'login_required': False,
        'errors': [],
        'form': None
    }

    # Сохраним в базе значение выбранного варианта для студента
    if request.method == 'PUT':
        student = Student.query.get(session['student_id'])
        student.variant = request.values.to_dict()['variant']
        db.session.add(student)
        db.session.commit()
        return json.dumps({
            'success': True,
        })

    # Проверка и перенаправление запроса в случае если он не соответствует состоянию тестирования
    if request.method == 'GET':
        actual_controller = check_status()
        if 'location' in request.values.to_dict().keys():
            return need_reload(actual_controller, 'studentstester.choice_of_variant')

        if actual_controller != 'studentstester.choice_of_variant':
            return redirect(url_for(actual_controller))

    return render_template('studentstester/choiceofvariant.html', values=values)


@studentstester.route('test_start/', methods=['GET', 'DELETE'])
def test_start():
    """
    Возвращает страницу с персоональными данными под которыми зарегистрировался студент для сверки,
    на этом этапе можно отменить ввод данных и ввести их заново
    """
    values = {
        'title': 'Онлайн тестирование',
        'page_info': 'Вы зарегистрировались на тестирование',
        'login_required': False,
        'errors': [],
        'form': None
    }
    # Удаление студента из базы данных в случае отказа от регистрации
    if request.method == 'DELETE':
        student = Student.query.get(session['student_id'])
        db.session.delete(student)
        db.session.commit()
        del session['student_id']
        return json.dumps({
            'success': True,
        })

    # Проверка и перенаправление запроса в случае если он не соответствует состоянию тестирования
    if request.method == 'GET':
        actual_controller = check_status()
        if 'location' in request.values.to_dict().keys():
            return need_reload(actual_controller, 'studentstester.test_start')

        if actual_controller != 'studentstester.test_start':
            return redirect(url_for(actual_controller))

    values['student'] = Student.query.get(session['student_id']).__dict__
    # TODO: Добавить цвет в зависимости от варианта
    return render_template('studentstester/teststart.html', values=values)


@studentstester.route('test_process/', methods=['GET', 'PUT'])
def test_process():
    """
    Возвращает страницу с вариантами ответа на вопрос для студента и обрабатывает события на этой странице
    """

    values = {
        'title': 'Онлайн тестирование',
        'page_info': 'Процесс тестирования',
        'login_required': False,
        'errors': [],
        'form': None
    }
    # Сохраним ответ студента в базе данных
    if request.method == 'PUT':
        student = Student.query.get(session['student_id'])
        if student.variant == 2:
            test_id = db.session.query(db.func.max(Test.id)).scalar()
        else:
            test_id = db.session.query(db.func.max(Test.id)).scalar() - 1
        questions = db.session.query(Answer.id).join(Question).filter(Question.test_id == test_id) \
            .filter(Question.num == request.values.to_dict()["quest_num"]).all()

        counter_ans = 0
        while 'answer_' + str(counter_ans) in request.values.to_dict().keys():
            db.session.add(StudentAnswer(
                student_id=student.id,
                answer_id=questions[counter_ans][0],
                value=True if request.values.to_dict()['answer_' + str(counter_ans)] == "True" else False
            ))
            counter_ans = counter_ans + 1
        db.session.commit()
        return json.dumps({
            'success': True
        })

    # Проверка и перенаправление запроса в случае если он не соответствует состоянию тестирования
    if request.method == 'GET':
        actual_controller = check_status()
        if 'location' in request.values.to_dict().keys():
            return need_reload(actual_controller, 'studentstester.test_process')

        if actual_controller != 'studentstester.test_process':
            return redirect(url_for(actual_controller))

    student = Student.query.get(session['student_id'])
    sessionparams = Sessions.query.get(1)

    values['student_answer'] = numbers_of_answers(student, sessionparams)
    values['student'] = student.__dict__

    return render_template('studentstester/testprocess.html', values=values)


@studentstester.route('test_end/', methods=['GET', 'POST'])
def test_end():
    """
    """
    # Проверка и перенаправление запроса в случае если он не соответствует состоянию тестирования
    if request.method == 'GET':
        actual_controller = check_status()
        if 'location' in request.values.to_dict().keys():
            return need_reload(actual_controller, 'studentstester.test_end')

        if actual_controller != 'studentstester.test_end':
            return redirect(url_for(actual_controller))

    values = {
        'title': 'Онлайн тестирование',
        'page_info': 'Тестирование закончено',
        'login_required': False,
        'errors': [],
        'form': None
    }
    return render_template('studentstester/testend.html', values=values)


def check_status():
    """
    Функция реализует проверку актуальности GET запроса текущему состоянию тестирования и проверку актуальности
    зарегистрированного в данной сессии студента запущенному тесту
    """
    test_status = Sessions.query.get(1).test_status

    if test_status == 1 or test_status == 2:
        return 'studentstester.no_test'

    # Проверка наличия зарегистрированного студента в данной сессии
    if 'student_id' in session:
        student = Student.query.get(session['student_id'])
        if not student:
            session.pop('student_id')
            return 'studentstester.personal_data' if test_status == 3 else 'studentstester.no_test'
    else:
        return 'studentstester.personal_data' if test_status == 3 else 'studentstester.no_test'

    # Проверка актуальности регистрации студента на текущий тест
    actual_test_id = db.session.query(db.func.max(Test.id)).scalar()
    if actual_test_id != student.test_id:
        session.pop('student_id')
        return 'studentstester.personal_data' if test_status == 3 else 'studentstester.no_test'

    # Проверка, выбран ли студентом вариант теста
    if not student.variant:
        return 'studentstester.choice_of_variant' if test_status == 3 else 'studentstester.no_test'

    if test_status == 3:
        return 'studentstester.test_start'

    if test_status == 4:
        return 'studentstester.test_process'

    if test_status == 5:
        return 'studentstester.test_end'

    return render_template('inprocess.html')


def need_reload(actual_controller, ajax_controller):
    """
    Функция определяет, требуется ли перезагрузить страницу для соответствия текущему состоянию тестирования и
    возвращает ответ для AJAX запроса
    """

    if actual_controller == ajax_controller:
        if 'quest_num' in request.values.to_dict().keys() and int(request.values.to_dict()['quest_num']) != Sessions.query.get(1).quest_num:
            return json.dumps({
                'reload': True,
            })
        return json.dumps({
            'reload': False,
        })
    else:
        return json.dumps({
            'reload': True,
        })


def numbers_of_answers(student, sessionparams):
    """
    Функция возвращает в словаре количество ответов списком и номер текущего вопроса
    """

    if student.variant == 2:
        test_id = db.session.query(db.func.max(Test.id)).scalar()
    else:
        test_id = db.session.query(db.func.max(Test.id)).scalar()-1

    quest_num = sessionparams.quest_num
    number_of_answers = db.session.query(Test).join(Question).filter(Test.id == test_id)\
        .join(Answer).filter(Question.num == quest_num).count()

    return {
        'quest_num': quest_num,
        'answers': [i for i in range(1, number_of_answers+1)]
    }


