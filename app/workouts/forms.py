from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError


class WorkoutForm(FlaskForm):
    category = SelectField('Category', choices=["Full body workout", "Legs", "ABS", "Upper body", "Cardio", "Stretching",
                                                "Yoga", "Pilates", "Mobility", "HIIT", "Rest"])
    description = TextAreaField("Description")
    submit = SubmitField("Submit")