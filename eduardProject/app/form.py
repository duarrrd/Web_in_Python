from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email

class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired("Це поле обов'язкове"), Email()])
    password = PasswordField(label='Password', validators=[DataRequired("Це поле обов'язкове")])
    remember = BooleanField(label="Запам'ятати мене")
    submit = SubmitField(label="Ввійти")

class RegistrationForm(FlaskForm):
    username = StringField(label='User name', validators=[DataRequired("Це поле обов'язкове"),
            Length(min=4, max=14, message="Від 4 до 14")
        ])
    email = StringField(label='Email', validators=[DataRequired("Це поле обов'язкове"), Email()])
    password = PasswordField(label='Password', validators=[DataRequired("Це поле обов'язкове"),
            Length(min=7, message="Mінімум 7 символів")
        ])
    confirm_password = PasswordField(label='Repeat Password', validators=[DataRequired("Це поле обов'язкове")])
    submit = SubmitField(label="Зареєструватись")

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

class TodoForm(FlaskForm):
    task = StringField('Завдання', validators=[DataRequired()])
    submit = SubmitField('Додати')