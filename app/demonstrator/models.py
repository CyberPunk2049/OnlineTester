from app.database import db
from sqlalchemy.orm import relationship


class Theme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)


class Special(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)


class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theme_id = db.Column(db.Integer, db.ForeignKey('theme.id'))
    theme = relationship("Theme", backref="tests")
    special_id = db.Column(db.Integer, db.ForeignKey('special.id'))
    special = relationship("Special", backref="tests")
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    num = db.Column(db.Integer)
    variant = db.Column(db.Integer)
    datetime = db.Column(db.DateTime, nullable=False)
    completed = db.Column(db.Boolean, default=False)

    questions = relationship("Question", cascade="all, delete", backref="test")
    students = relationship("Student", cascade="all, delete", backref="test")


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'))
    num = db.Column(db.Integer)
    name = db.Column(db.String())
    text = db.Column(db.String())
    img_path = db.Column(db.String())

    answers = relationship("Answer", cascade="all, delete", backref="question")


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    num = db.Column(db.Integer)
    text = db.Column(db.String())
    value = db.Column(db.Boolean())


