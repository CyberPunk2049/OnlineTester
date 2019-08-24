from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired, Email, Length


class PersonalDataForm(FlaskForm):
    name = StringField('Имя', [DataRequired(), Length(max=50)])
    surname = StringField('Фамилия', [DataRequired(), Length(max=50)])
    patronymic = StringField('Отчество', [DataRequired(), Length(max=50)])
    group = StringField('Группа', [DataRequired(), Length(max=20)])
    email = StringField('E-mail', [DataRequired(), Email(message='Неверно введён E-mail'), Length(max=100)])
    submit = SubmitField('Подтвердить')


class ChoiceOfVariant(FlaskForm):
    variant = RadioField('Вариант', choices=[(1, 'Вариант 1'), (2, 'Вариант 2')], coerce=int)
    submit = SubmitField('Подтвердить')
