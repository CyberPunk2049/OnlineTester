import json
import os
from flask import Blueprint, render_template, redirect, url_for, request, current_app
from sqlalchemy import func
from app.wrappers import login_require
from app.administrator.models import Sessions
from app.demonstrator.models import Test, Question, Answer
from app.studentstester.models import Student, StudentAnswer
from app.database import db

estimator = Blueprint(
    'estimator',
    __name__,
    url_prefix='/estimator/'
)


@estimator.route('/')
@login_require
def index():
    return redirect(url_for('estimator.tests_list'))


@estimator.route('tests_list/', methods=['GET', 'DELETE'])
@login_require
def tests_list():
    """
    Возвращает страницу со списком пройденных тестов
    """

    values = {
        'title': 'Результаты тестов',
        'page_info': 'Проведённые тестирования',
        'login_required': True,
        'errors': [],
        'form': None
    }

    subject = Sessions.query.get(1).subject

    # Очистим список пройденных тестов для данного предмета
    if request.method == 'DELETE':
        return delete_tests(subject)

    values['tests_list'] = []
    for idx, test in enumerate(Test.query.filter(Test.subject_id == subject, Test.completed == True).all()):
        # TODO: Переделать в nametuple
        if idx % 2 == 1:
            values['tests_list'].append(
                (
                    test.special.name,
                    test.theme.name,
                    test.num,
                    test.datetime.strftime('%d.%m.%y'),
                    test.datetime.strftime("%X"),
                    len(test.students),
                    test.id
                )
            )
    return render_template('estimator/tests_list.html', values=values)


@estimator.route('test_results/')
@login_require
def test_result():
    """
    Возвращает страницу со результатами теста
    """

    values = {
        'title': 'Результаты тестов',
        'page_info': 'Результаты тестирования',
        'login_required': True,
        'errors': [],
        'form': None
    }
    # Проверка наличия необходимых параметров в GET запросе
    if 'test_id' in request.args and 'full_answer' in request.args:
        test_id = int(request.args['test_id'])
        values['test_id'] = test_id
        full_answer = bool(int(request.args['full_answer']))
        values['full_answer'] = full_answer
    else:
        return redirect(url_for('estimator.tests_list'))

    test = Test.query.get(test_id)
    values['num'] = test.num
    values['theme'] = test.theme.name
    values['special'] = test.special.name

    students = Student.query.filter(Student.test_id.in_([test_id, test_id - 1]))

    # Для каждого варианта получим списки с числом возможных и правильных ответов
    [answers_count_1, answers_count_2] = [answers_count_zip(test_id-1), answers_count_zip(test_id)]

    values['test_results'] = []
    # Посчитаем баллы для каждого студента
    for student in students:
        if student.variant == 1:
            answers_count = answers_count_1
        elif student.variant == 2:
            answers_count = answers_count_2
        else:
            values['errors'].append(u"Не возможно установить вариант у студента. Cтуд.билет №: "
                                    + str(student.student_id))
            continue

        # Массив кортежей засчитанных ответов студента на каждый вопрос (номер вопроса, число засчитанных ответов)
        student_ans_count = db.session.query(Question.num, func.count(StudentAnswer.student_id)).filter(
            StudentAnswer.answer_id == Answer.id,
            Question.id == Answer.question_id
        ).filter(
            StudentAnswer.student_id == student.id
        ).group_by(
            Question.num
        ).order_by(
            Question.num
        ).all()

        student_answers_list = student_answers_zip(student)

        if full_answer:
            answer_grade = full_answer_grade(answers_count, student_ans_count, student_answers_list)
        else:
            answer_grade = part_answer_grade(answers_count, student_ans_count, student_answers_list)

        values['test_results'].append({
            'id': student.id,
            'student_id': student.student_id,
            'name': student.name,
            'surname': student.surname,
            'patronymic': student.patronymic,
            'group': student.group,
            'variant': student.variant,
            'email': student.email,
            'counted_answers': answer_grade['counted_answers'],
            'total_number': answer_grade['total_number'],
            'grade_percent': answer_grade['grade_percent']
        })
    return render_template('estimator/test_results.html', values=values)


@estimator.route('student_answers/')
@login_require
def student_answers():
    """
    Возвращает страницу с ответами студента на тест
    """
    values = {
        'title': 'Результаты тестов',
        'login_required': True,
        'errors': [],
        'form': None
    }
    if 'student_id' in request.args:
        student_id = request.args['student_id']
    else:
        return redirect(url_for('estimator.tests_list'))

    student = Student.query.get(student_id)

    if not student:
        return redirect(url_for('estimator.tests_list'))

    values['page_info'] = 'Бланк ответов: ' + str(student.surname) + ' ' + str(student.name[0]) + '. ' \
                          + str(student.patronymic[0]) + '., ' + str(student.group) + ' группа.'

    test = Test.query.get(student.test_id + student.variant - 2)

    values['num'] = test.num
    values['theme'] = test.theme.name
    values['special'] = test.special.name
    values['variant'] = student.variant
    values['test_id'] = student.test_id

    studentanswers = db.session.query(StudentAnswer.answer_id, StudentAnswer.value).filter(
        StudentAnswer.student_id == student_id).subquery()

    answers = db.session.query(
        Question.num, Question.name, Question.text, Question.img_path, Answer.num, Answer.text, Answer.value,
        studentanswers.c.value
    ).join(Answer).outerjoin(
        studentanswers, studentanswers.c.answer_id == Answer.id
    ).filter(
        Question.test_id == test.id
    ).order_by(
        Question.num, Answer.num
    ).all()
    values['questions'] = []

    # Объединим ответы студентов в структуру для удобного вывода в шаблоне
    # values['questions'] = [
    #    {
    #        'name': 'Задание 1',
    #        'text': 'Текст вопроса',
    #        'answers_text': ['Текст 1-го ответа', 'Текст 2-го ответа', 'Текст 3-го ответа'],
    #        'answers_true': [True, True, False],
    #        'answers_student': [True, False, False],
    #    },
    #    {
    #        'name': 'Задание 2',
    #        'text': 'Текст вопроса',
    #        'answers_text': ['Текст 1-го ответа', 'Текст 2-го ответа', 'Текст 3-го ответа'],
    #        'answers_true': [True, True, False],
    #        'answers_student': [True, False, False],
    #    },
    #
    #   .....
    #
    # ]

    for answer in answers:
        if not values['questions'] or len(values['questions']) != answer[0]:
            values['questions'].append({
                'name': answer[1],
                'text': answer[2],
                'img_path': answer[3],
                'answers': [{
                    'text': answer[5],
                    'true': answer[6],
                    'student': answer[7],
                }],
            })
            continue
        if len(values['questions']) == answer[0]:
            values['questions'][answer[0] - 1]['answers'].append({
                'text': answer[5],
                'true': answer[6],
                'student': answer[7],
            })
    return render_template('estimator/student_answers.html', values=values)


def answers_count_zip(test_id):
    """
    Возвращает для теста список кортежей вида [(номер вопроса, число возможных ответов, число правильных ответов(True))]
    """

    # Получим список с числом возможных ответов на каждый вопрос
    answers_count = db.session.query(func.count(Question.num)).join(Answer).filter(
        Question.test_id == test_id).group_by(Question.num).order_by(Question.num).all()
    # Получим список с числом правильных ответов на каждый вопрос
    answers_true_count = db.session.query(func.count(Question.num)).join(Answer).filter(
        Question.test_id == test_id, Answer.value == True).group_by(Question.num).order_by(Question.num).all()
    print("answers_count_zip " + str(answers_count))
    print("answers_true_count_zip " + str(answers_true_count))

    return [(num+1, count[0][0], count[1][0]) for num, count in enumerate(zip(answers_count, answers_true_count))]


def student_answers_zip(student):
    """
    Возвращает для студента список кортежей вида
    [(номер вопроса, число верных ответов(True=True), число неверных ответов(True=False))]
    для каждого вопроса, вне зависимости от того засчитался ли ответ или нет, если не засчитался или студент не отвечал,
    то (num, 0, 0)
    """
    # Массив кортежей верных положительных(True) ответов
    # студента на каждый вопрос (номер вопроса, число верных ответов)
    student_true_ans_count = db.session.query(Question.num, func.count(StudentAnswer.student_id)).filter(
        StudentAnswer.answer_id == Answer.id,
        Question.id == Answer.question_id,
        StudentAnswer.value == True
    ).filter(
        StudentAnswer.value == Answer.value
    ).filter(
        StudentAnswer.student_id == student.id
    ).group_by(
        Question.num
    ).order_by(
        Question.num
    ).all()

    # Массив кортежей неверных положительных(True) ответов
    # студента на каждый вопрос (номер вопроса, число верных ответов)
    student_false_ans_count = db.session.query(Question.num, func.count(StudentAnswer.student_id)).filter(
        StudentAnswer.answer_id == Answer.id,
        Question.id == Answer.question_id,
        StudentAnswer.value == True
    ).filter(
        StudentAnswer.value != Answer.value
    ).filter(
        StudentAnswer.student_id == student.id
    ).group_by(
        Question.num
    ).order_by(
        Question.num
    ).all()

    questions_count = db.session.query(func.count(Question.id)).filter(Question.test_id == student.test_id).one()[0]
    print("question_count " + str(questions_count))

    student_true_ans_count_dict = dict(student_true_ans_count)
    student_false_ans_count_dict = dict(student_false_ans_count)
    student_answers_list = []
    for num in range(1, questions_count+1):
        if num in student_true_ans_count_dict:
            true_ans = student_true_ans_count_dict[num]
        else:
            true_ans = 0

        if num in student_false_ans_count_dict:
            false_ans = student_false_ans_count_dict[num]
        else:
            false_ans = 0
        student_answers_list.append((num, true_ans, false_ans))

    return student_answers_list


def full_answer_grade(answers_count, student_ans_count, student_answers_list):
    """
    Возвращает число защитанных вопросов, общее количество вопросов и процент правильных ответов в словаре при условие
    учитывания только полных ответов для одного студента
    """
    total_number = len(answers_count)
    counted_answers = len(student_ans_count)
    print("answers_count " + str(answers_count))
    print("student_answers_list" + str(student_answers_list))

    # Счётчик правильных ответов
    true_counter = 0
    for idx, answer_count in enumerate(answers_count):
        if answer_count[2] == student_answers_list[idx][1] and student_answers_list[idx][2] == 0:
            true_counter += 1

    grade_percent = round(true_counter / total_number * 100, 2)
    return {
        'counted_answers': counted_answers,
        'total_number': total_number,
        'grade_percent': grade_percent
    }


def part_answer_grade(answers_count, student_ans_count, student_answers_list):
    """
    Возвращает число защитанных вопросов, общее количество вопросов и процент правильных ответов в словаре при условие
    учитывания неполных ответов для одного студента
    """
    total_number = len(answers_count)
    counted_answers = len(student_ans_count)

    print("answers_count " + str(answers_count))
    print("student_answers_list" + str(student_answers_list))
    # Счётичик правильных ответов
    true_counter = 0
    for idx, answer_count in enumerate(answers_count):
        answer_proportion = student_answers_list[idx][1]/answer_count[2]\
            - student_answers_list[idx][2]/(answer_count[1]-answer_count[2])
        print("answer_proportion " + str(idx) + ' ' + str(answer_proportion))
        if answer_proportion > 0:
            true_counter += answer_proportion

    grade_percent = round(true_counter / total_number * 100, 2)
    return {
        'counted_answers': counted_answers,
        'total_number': total_number,
        'grade_percent': grade_percent
    }


def delete_tests(subject_id):
    """
    Функция каскадно удаляет из базы данных тесты для выбранного предмета
    """
    tests = Test.query.filter(Test.subject_id == subject_id).all()
    images = db.session.query(Question.img_path).filter(
        Test.subject_id == subject_id,
        Question.test_id == Test.id,
        Question.img_path != '').all()
    print(images)
    # Удалим все изображения, соответствующие удаляемым вопросам тестов
    for image in images:
        try:
            os.remove(os.path.join(current_app.root_path, current_app.config['MEDIA_FOLDER'], image[0]))
        except FileNotFoundError:
            pass
    # Удалим все тесты, студентов и их результаты из базы данных
    for test in tests:
        db.session.delete(test)
    db.session.commit()
    return json.dumps({
        'success': True
    })
