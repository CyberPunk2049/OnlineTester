from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField, IntegerField, SelectField


class UploadFilesForm(FlaskForm):
    num = IntegerField('Номер', default=0)
    theme = SelectField('Тема', coerce=int)
    special = SelectField('Специальность', coerce=int)
    variant1 = FileField('Вариант I', validators=[FileRequired()])
    variant2 = FileField('Вариант II', validators=[FileRequired()])
    submit = SubmitField('Загрузить')


class TestStartForm(FlaskForm):
    quest_time = IntegerField('Время вопроса (сек)')
    submit = SubmitField('Начать тестирование')


class TestFinishForm(FlaskForm):
    submit = SubmitField('Сохранить результаты теста')

