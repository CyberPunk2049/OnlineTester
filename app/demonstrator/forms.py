from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField, IntegerField, SelectField


class UploadFilesForm(FlaskForm):
    num = IntegerField('Номер', default=0)
    theme = SelectField('Тема', coerce=int)
    special = SelectField('Специальность', coerce=int)
    variant1 = FileField('Вариант 1', validators=[FileRequired()])
    variant2 = FileField('Вариант 2', validators=[FileRequired()])
    submit = SubmitField('Загрузить')


class TestStartForm(FlaskForm):
    num = IntegerField('Время вопроса', default=20)
    submit = SubmitField('Начать тестирование')

