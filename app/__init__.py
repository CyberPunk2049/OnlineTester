from flask import Flask, redirect, url_for, render_template
from flask_bootstrap import Bootstrap

def create_app(config):

    app = Flask(__name__)
    app.config.from_object(config)
    bootstrap = Bootstrap(app)

    from app.database import db

    from app.administrator.controllers import administrator
    from app.studentstester.controllers import tester
    from app.demonstrator.controllers import demonstrator
    from app.estimator.controllers import estimator

    app.register_blueprint(administrator)
    app.register_blueprint(tester)
    app.register_blueprint(demonstrator)
    app.register_blueprint(estimator)

    with app.app_context():
        db.init_app(app)
        db.create_all()

    @app.route('/')
    def index():
        return redirect(url_for('studentstester.index'))

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html')

    return app
