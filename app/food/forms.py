from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired


class FoodForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    proteins = FloatField('Proteins')
    carbs = FloatField('Carbs')
    fats = FloatField('Fats')
    submit = SubmitField('Submit')


class FoodTracker(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    portion = IntegerField('Portion in grams:', validators=[DataRequired()])
    submit = SubmitField('Submit')


class DateForm(FlaskForm):
    date = DateField('Time', validators=[DataRequired()])
    submit = SubmitField('Submit')

