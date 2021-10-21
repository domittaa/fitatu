from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, FileField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=8, message='Password must be longer than 8 characters')])
    password_repeat = PasswordField('Repeat password',
                                    validators=[DataRequired(), EqualTo('password', message="Passwords must match")])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('This username is already taken!')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError('This email is already register!')


class EditProfileForm(FlaskForm):
    avatar = FileField('Avatar')
    username = StringField('Username', validators=[DataRequired()])
    weight = IntegerField('Weight in kilograms')
    height = IntegerField('Height in centimeters')
    sex = SelectField('Sex', choices=['Female', 'Male'])
    age = IntegerField('Age')
    submit = SubmitField('Save')
    pal = SelectField('PAL-Physical Activity Level', choices=[1.2, 1.4, 1.6, 1.8, 2.0])


