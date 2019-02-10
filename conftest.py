from config import TestConfig
from app import create_app
from app.database import db
from app.administrator.models import User, Subject, Sessions, TestStatus
from app.demonstrator.models import Theme, Special
import random

import pytest


@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.init_app(app)
        db.create_all()

        admin = User(username='admin', password='1w2w3e4r')
        db.session.add(admin)
        db.session.commit()

        subjects = [
            'Биология',
            'Физиология',
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
            'Стоматологи',
            'Лечебники',
        ]

        for name in specials:
            db.session.add(Special(name=name))
        db.session.commit()

        statuses = [
            'Загрузка тестов',
            'Отображение тестов',
            'Процесс тестирования',
            'Окончание теста'
        ]

        for status in statuses:
            db.session.add(TestStatus(text_status=status))
        db.session.commit()

        db.session.add(Sessions(session_id=random.randint(0, 1000), subject=1, test_status=1, quest_num=1, quest_time=20))
        db.session.commit()

        yield app

        db.session.close()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


class AuthActions(object):

    def __init__(self, client):
        self._client = client

    def login(self, username='admin', password='1w2w3e4r', subject=1):
        return self._client.post(
            '/administrator/login/',
            data={
                'subject': subject,
                'username': username,
                'password': password,
            }
        )

    def logout(self):
        return self._client.get('/administrator/logout/')


@pytest.fixture
def client_auth(client):
    return AuthActions(client)
