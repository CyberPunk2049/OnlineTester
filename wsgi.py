import config
from app import create_app

if __name__ == '__main__':
    application = create_app(config.ProductionConfig)
    application.run()
