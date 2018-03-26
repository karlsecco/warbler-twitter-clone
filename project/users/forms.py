from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Email, Length


class UserForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    image_url = StringField('image_url')
    password = PasswordField('password', validators=[Length(min=6)])


class EditForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    first_name = StringField('first name')
    last_name = StringField('last name')
    bio = StringField('bio', validators=[Length(max=140)], widget=TextArea())
    location = StringField('location')
    image_url = StringField('image_url')
    header_image_url = StringField('header_image_url')
    password = PasswordField('password', validators=[Length(min=6)])


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[Length(min=6)])