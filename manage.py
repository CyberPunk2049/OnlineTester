import config
from flask_script import Manager
from app import create_app

app = create_app(config.DevelopmentConfig)
manager = Manager(app)


if __name__ == '__main__':
    manager.run()
