from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(u'用户名不能为空')])
    pwd = PasswordField('pwd', validators=[DataRequired(u'密码不能为空')])
    submit = SubmitField('Login in')


class RegisterForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    pwd = PasswordField('pwd', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(message=u'邮箱不能为空'),
                                             Email(message=u'请输入有效的邮箱地址，比如：username@domain.com')])
    submit = SubmitField('register')
