from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, SelectField, FloatField
from wtforms.validators import DataRequired

class BMIForm(FlaskForm):
    weight = IntegerField('Weight in kilograms', validators=[DataRequired()])
    height = FloatField('Height in metres', validators=[DataRequired()])
    submit = SubmitField('Calculate')


class BMRForm(FlaskForm):
    weight = IntegerField('Weight in kilograms', validators=[DataRequired()])
    height = IntegerField('Height in centimeters', validators=[DataRequired()])
    sex = SelectField('Sex', choices=['Female', 'Male'], validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    submit = SubmitField('Calculate')


class TERForm(FlaskForm):
    weight = IntegerField('Weight in kilograms', validators=[DataRequired()])
    height = IntegerField('Height in centimeters', validators=[DataRequired()])
    sex = SelectField('Sex', choices=['Female', 'Male'], validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    pal = SelectField('PAL', choices=[1.2, 1.4, 1.6, 1.8, 2.0], validators=[DataRequired()])
    submit = SubmitField('Calculate')
