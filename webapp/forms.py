from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Regexp, EqualTo, ValidationError, Email

from .models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    telno = StringField('Telnumber', validators=[DataRequired(), Regexp(regex=r'1\d{8}')])
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Password', validators=[DataRequired(), EqualTo('password')])

    register = SubmitField('注册')

    def validate_username(self, username):
        user = User.query.filter_by(name=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_telno(self, telno):
        user = User.query.filter_by(telno=telno.data).first()
        if user is not None:
            raise ValidationError(f'telno: {telno} has been registered.')
