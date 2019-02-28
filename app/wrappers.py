from flask import session, redirect, url_for
from functools import wraps
from app.administrator.models import Sessions


def login_require(f):
    @wraps(f)
    def decorated_function():
        actual_login = False
        if len(session) != 0:
            actual_login = True
            sessionparams = Sessions.query.get(1)
            for key in ['subject', 'test_status', 'quest_num', 'quest_time', 'quest_max']:
                if session.get(key) != getattr(sessionparams, key, None):
                    actual_login = False
                    break

        if actual_login == True:
            return f()
        else:
            return redirect(url_for('administrator.login'))
    return decorated_function


