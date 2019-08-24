from sqlalchemy import event
from app.database import db
from app.demonstrator.models import Test


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    patronymic = db.Column(db.String(50))
    group = db.Column(db.String(20))
    email = db.Column(db.String(100))
    variant = db.Column(db.Integer)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'))


class StudentAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'))
    value = db.Column(db.Boolean)


@event.listens_for(Student, 'before_insert')
def add_test_id(mapper, connection, target):
    test_id = db.session.query(db.func.max(Test.id)).scalar()
    target.test_id = test_id
    print('Test_id: ' + str(test_id))

