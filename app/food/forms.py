from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired


class FoodForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    proteins = FloatField('Proteins', validators=[DataRequired()])
    carbs = FloatField('Carbs', validators=[DataRequired()])
    fats = FloatField('Fats', validators=[DataRequired()])
    submit = SubmitField('Submit')
