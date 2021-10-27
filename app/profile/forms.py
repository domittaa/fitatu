from flask_wtf import FlaskForm
from wtforms import StringField,  SubmitField, IntegerField, SelectField, FileField
from wtforms.validators import DataRequired, ValidationError, Optional
from app.models import User


class EditProfileForm(FlaskForm):
    avatar = FileField('Avatar')
    username = StringField('Username', validators=[DataRequired()])
    weight = IntegerField('Weight in kilograms', validators=[Optional()])
    height = IntegerField('Height in centimeters', validators=[Optional()])
    sex = SelectField('Sex', choices=['Female', 'Male'], validators=[Optional()])
    age = IntegerField('Age', validators=[Optional()])
    submit = SubmitField('Save')
    pal = SelectField('PAL-Physical Activity Level', choices=[1.2, 1.4, 1.6, 1.8, 2.0], validators=[Optional()])

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')





