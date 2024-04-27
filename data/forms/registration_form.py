from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired


class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    maniac = BooleanField('Я маньяк')
    submit = SubmitField('Зарегистрироваться')
