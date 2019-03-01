import os


class Config(object):

    # Режим отладки
    DEBUG = False
    # Включение защиты против "Cross-site Request Forgery (CSRF)"
    CSRF_ENABLED = True
    # Случайный ключ, которые будет исползоваться для подписи
    # данных, например cookies.
    SECRET_KEY = 'e03f77bfa4333a973e480e77ff0e8a177913417aa1fc8bf9'

    # Расширения разрешённых для загрузки файлов
    ALLOWED_EXTENSIONS = set(['rtf'])

    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:qwerty@localhost/online_tester-dev'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:beBl9iPxNr@localhost/online_tester-prod'


class DevelopmentConfig(Config):
    DEBUG = True


class TestConfig(Config):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:qwerty@localhost/online_tester-test'

    WTF_CSRF_ENABLED = False

    ROOT_LOCATION = 'http://localhost'
