from flask import session, current_app
from app.administrator.models import Sessions


class TestRoute(object):

    def test_homepage(self, client, client_auth):
        response = client.get('/')
        assert response.status_code == 302 and \
            response.location == current_app.config['ROOT_LOCATION']+'/studentstester/'

        client_auth.login()
        response = client.get('/administrator/')
        assert response.status_code == 200

    def test_studentester(self, client):
        response = client.get('/studentstester/')
        assert response.status_code == 200

    def test_administrator(self, client, client_auth):
        response = client.get('/administrator/')
        assert response.status_code == 302 and \
            response.location == current_app.config['ROOT_LOCATION']+'/administrator/login/'

        client_auth.login()
        response = client.get('/administrator/')
        assert response.status_code == 200

    def test_login(self, client, client_auth):
        response = client.get('/administrator/login/')
        assert response.status_code == 200

        client_auth.login()
        response = client.get('/administrator/login/')
        assert response.status_code == 302 and \
            response.location == current_app.config['ROOT_LOCATION']+'/administrator/'

    def test_logout(self, client, client_auth):
        response = client.get('/administrator/logout/')
        assert response.status_code == 302 and \
            response.location == current_app.config['ROOT_LOCATION']+'/administrator/login/'

        client_auth.login()
        response = client.get('/administrator/logout/')
        assert response.status_code == 302 and \
            response.location == current_app.config['ROOT_LOCATION'] + '/administrator/login/'

    def test_demonstrator(self, client, client_auth):
        response = client.get('/demonstrator/')
        assert response.status_code == 302 and \
            response.location == current_app.config['ROOT_LOCATION']+'/administrator/login/'

        client_auth.login()
        response = client.get('/demonstrator/')
        # TODO:Сделать тест для всех вариантов
        assert response.status_code == 302

    def test_estimator(self, client, client_auth):
        response = client.get('/estimator/')
        assert response.status_code == 302 and \
            response.location == current_app.config['ROOT_LOCATION']+'/administrator/login/'

        client_auth.login()
        response = client.get('/estimator/')
        assert response.status_code == 200


class TestAuth(object):

    def test_correct_auth(self, client, client_auth):
        # При корректном вводе логина и пароля должно происходить перенаправление на страницу /administrator/
        # TODO:Должен устанавливаться идентификатор сессии
        response = client_auth.login()
        assert response.status_code == 302 and \
            response.location == current_app.config['ROOT_LOCATION']+'/administrator/'

        with client.session_transaction() as sess:
            assert sess['id'] == Sessions.query.get(1).session_id

    def test_incorrect_pass(self, client_auth):
        # При некорректном вводе пароля должно происходить возвращение к окну приглашения ввода логина и пароля
        # с указанием ошибки
        response = client_auth.login(password='12312342134')
        assert response.status_code == 200

    def test_incorrect_login(self, client_auth):
        # При некорректном вводе логина должно происходить возвращение к окну приглашения ввода логина и пароля
        # с указанием ошибки
        response = client_auth.login(username='vasd')
        assert response.status_code == 200

    def test_logout(self, client, client_auth):
        # При разлогинивании должен удаляться идентификатор сессии
        # TODO: Должно происходить возвращение к приглашению ввода логина и пароля
        client_auth.login()
        with client:
            client.get('/administrator/logout/')
            assert id not in session

