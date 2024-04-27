from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class NewFishForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    text = TextAreaField('Содержание', validators=[DataRequired()])
    submit = SubmitField('Отправить желание')
