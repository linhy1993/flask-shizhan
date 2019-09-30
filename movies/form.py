from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    pwd = PasswordField('pwd', validators=[DataRequired()])
    submit = SubmitField('Login in')


class RegisterForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    pwd = PasswordField('pwd', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    submit = SubmitField('register')
