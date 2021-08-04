from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo

from tutorialportal.models import User, Tutor


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        search = User.query.filter_by(username=username.data).all()
        if len(search) != 0:
            raise ValidationError('This username belongs to an existing tutor/student.')

    def validate_email(self, email):
        search = Tutor.query.filter_by(email=email.data).all()
        if len(search) != 0:
            raise ValidationError('This email belongs to an existing tutor.')
