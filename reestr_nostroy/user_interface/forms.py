from wtforms import TextAreaField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[Email()])
    psw = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=4, max=100)])
    remember = BooleanField("Запомнить", default = False)
    submit = SubmitField("Войти")