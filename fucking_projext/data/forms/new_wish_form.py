from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, validators


class NewFishForm(FlaskForm):
    name = StringField('Название', validators=[validators.Length(min=3, max=20)])
    text = TextAreaField('Содержание', validators=[validators.Length(min=20, max=500)])
    submit = SubmitField('Отправить желание')
