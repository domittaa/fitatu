from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, FieldList
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Optional


class ListForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Create')


class ListProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[Optional()])
    submit = SubmitField('Add')


class FridgeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[Optional()])
    expired_date = DateField('Expiration date',validators=[Optional()], format='%Y-%m-%d')
    category = SelectField('Category', choices=['Grains', 'Vegetables', 'Fruits', 'Dairy', 'Meat', 'Drinks'])
    submit = SubmitField('Add product')


class MenuForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])
    products = StringField('Products:', validators=[DataRequired()])
    category = SelectField('Category', choices=['Breakfast', 'Second breakfast', 'Lunch', 'Dessert', 'Dinner'])
    submit = SubmitField('Submit')

