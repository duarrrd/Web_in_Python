from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    name = StringField(label='User name', validators=[DataRequired("Це поле обов'язкове")])
    password = PasswordField(label='Password', validators=[DataRequired("Це поле обов'язкове"),
                Length(min=4, max=10, message="Повинно бути від 4 до 10 символів")])
    remember = BooleanField(label="Запам'ятати мене")
    submit = SubmitField(label="Ввійти")

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(label='Old password', validators=[DataRequired("Це поле обов'язкове"),
            Length(min=4, max=10, message="Повинно бути від 4 до 10 символів")])
    new_password = PasswordField(label='New password', validators=[DataRequired("Це поле обов'язкове"),
            Length(min=4, max=10, message="Повинно бути від 4 до 10 символів")])
    submit = SubmitField(label="Зберегти")

class FeedbackForm(FlaskForm):
    name = StringField('Ім’я', validators=[DataRequired()])
    comment = TextAreaField('Коментар', validators=[DataRequired()])
    submit = SubmitField('Надіслати відгук')