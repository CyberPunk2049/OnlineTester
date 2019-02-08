from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField, IntegerField, SelectField


class UploadFilesForm(FlaskForm):
    num = IntegerField('Num', default=0)
    theme = SelectField('Theme', coerce=int)
    special = SelectField('Special', coerce=int)
    variant1 = FileField(validators=[FileRequired()])
    variant2 = FileField(validators=[FileRequired()])
    submit = SubmitField('Загрузить')
