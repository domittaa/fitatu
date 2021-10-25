from flask import url_for, redirect, render_template

from app.food import bp
from app import db
from app.models import Food
from app.food.forms import FoodForm
from flask_login import login_required


@login_required
@bp.route('/add', methods=['GET', 'POST'])
def add():
    form = FoodForm()
    if form.validate_on_submit():
        name = form.name.data
        proteins = form.proteins.data
        carbs = form.carbs.data
        fats = form.fats.data
        calories = proteins*4 + fats*9 + carbs*4
        food = Food(name=name, proteins=proteins, carbs=carbs, fats=fats, calories=calories)
        db.session.add(food)
        db.session.commit()
        return redirect(url_for('food.add'))
    food = Food.query.all()
    return render_template('food/add.html', form=form, food=food)

