from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    name = StringField(label='User name', validators=[DataRequired("Це поле обов'язкове")])
    password = PasswordField(label='Password', validators=[DataRequired("Це поле обов'язкове"),
                Length(min=4, max=10, message="Повинно бути від 4 до 10 символів")])
    remember = BooleanField(label="Запам'ятати мене")
    submit = SubmitField(label="Ввійти")