from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    title = StringField(label='Title', validators=[DataRequired("Title is required")], id="title")
    text = TextAreaField(label='Text', validators=[DataRequired("Text is required")], id="text")
    image = FileField(label='Image', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])], id="image")
    type = SelectField(label='Post type (select one)', choices=[
        ('Other', "Other"), ('Pets', 'Pets'), ('Gym', 'Gym'),
        ('Food', 'Food')
    ])
    enabled = BooleanField(label='Show post', id="enabled")
    submit = SubmitField(label="Save", id="submit")
