from flask import session,redirect,url_for
from functools import wraps


def login_require(f, loginpage='administrator.login'):
    @wraps(f)
    # TODO: Добавить проверку актуальности сессии
    def decorated_function():
        if 'id' in session:
            return f()
        else:
            return redirect(url_for(loginpage))
    return decorated_function
