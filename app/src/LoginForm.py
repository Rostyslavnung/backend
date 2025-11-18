from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField(
        'Ім’я користувача',
        validators=[DataRequired(message="Поле обов’язкове"), Length(min=3, max=50)]
    )
    password = PasswordField(
        'Пароль',
        validators=[DataRequired(message="Поле обов’язкове")]
    )
    submit = SubmitField('Увійти')
