import config
from app import create_app
from app.database import db
import random
from app.administrator.models import User, Sessions, Subject, TestStatus
from app.demonstrator.models import Theme, Special

# Скрипт для создания и заполнения фиксированных таблиц в базе данных.

app = create_app(config.DevelopmentConfig)


with app.app_context():
    db.drop_all()
    db.init_app(app)
    db.create_all()

    subjects = [
        'Биология',
        'Норм. физиология',
    ]
    for name in subjects:
        db.session.add(Subject(name=name))
    db.session.commit()

    themes = [
        'Коллоквиум',
        'Экзамен',
        'Зачёт',
    ]
    for name in themes:
        db.session.add(Theme(name=name))
    db.session.commit()

    specials = [
        'Лечебное дело',
        'Стоматология',
        'Сестринское дело',
        'Фармация'
    ]

    for name in specials:
        db.session.add(Special(name=name))
    db.session.commit()

    statuses = [
        'Загрузка тестов',
        'Отображение тестов',
        'Процесс тестирования',
        'Окончание теста',
    ]

    for status in statuses:
        db.session.add(TestStatus(text_status=status))
    db.session.commit()

    users = [
        {
            'login': 'teacher',
            'password': 'cfbh32'
        }
    ]
    for user in users:
        db.session.add(User(username=user['login'], password=user['password']))
    db.session.commit()

    db.session.add(Sessions(session_id=random.randint(0, 1000), subject=1, test_status=1, quest_num=1, quest_time=20))
    db.session.commit()
