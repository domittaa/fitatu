from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Optional


class ListForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Create List')


class ListProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[Optional()])
    submit = SubmitField('Add product')


class FridgeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[Optional()])
    expired_date = DateField('Expired date',validators=[Optional()], format='%Y-%m-%d')
    category = SelectField('Category', choices=['Grains', 'Vegetables', 'Fruits', 'Dairy', 'Meat', 'Drinks'])
    submit = SubmitField('Add product')
