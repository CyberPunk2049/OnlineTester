from app.database import db


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)


class TestStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text_status = db.Column(db.String(200))


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50))


class Sessions(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, nullable=False, unique=True)
    subject = db.Column(db.Integer, db.ForeignKey('subject.id'))
    test_status = db.Column(db.Integer, db.ForeignKey('test_status.id'))
    quest_num = db.Column(db.Integer, default=0)


