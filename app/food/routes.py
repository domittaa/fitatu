from datetime import datetime, date

from flask import url_for, redirect, render_template, flash
from sqlalchemy import extract

from app.food import bp
from app import db
from app.models import Food, Portion
from app.food.forms import FoodForm, FoodTracker
from flask_login import login_required, current_user


@login_required
@bp.route('/add', methods=['GET', 'POST'])
def add():
    form = FoodForm()
    if form.validate_on_submit():
        name = form.name.data.capitalize()
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


@bp.route('/<time>', methods=['GET', 'POST'])
@login_required
def index(time):
    form = FoodTracker()
    if form.validate_on_submit():
        name = form.name.data.capitalize()
        portion = form.portion.data
        check = Food.query.filter_by(name=name).first()
        if check is None:
            flash(f'No {name} in our database. Use link below to add {name} to our database.')
            return redirect(url_for('food.index', time='today'))
        else:
            proteins = check.proteins*portion/100
            carbs = check.carbs*portion/100
            fats = check.fats*portion/100
            calories = check.calories*portion/100
            food = Portion(name=name, portion=portion, proteins=proteins, carbs=carbs, fats=fats, calories=calories,
                           user=current_user, time=date.today())

            db.session.add(food)
            db.session.commit()

    now = datetime.utcnow()
    if time == 'today':
        portion = Portion.query.filter(extract('year', Portion.time) == now.year, extract('month', Portion.time) == now.month,
                                       extract('day', Portion.time) == now.day).filter_by(user_id=current_user.id).all()
    elif time == 'yesterday':
        portion = Portion.query.filter(extract('year', Portion.time) == now.year, extract('month', Portion.time) == now.month,
                                       extract('day', Portion.time) == now.day-1).filter_by(user_id=current_user.id).all()
    elif time == 'tomorrow':
        portion = Portion.query.filter(extract('year', Portion.time) == now.year, extract('month', Portion.time) == now.month,
                                       extract('day', Portion.time) == now.day+1).filter_by(user_id=current_user.id).all()

    calories_sum = round(sum([i.calories for i in portion]), 2)
    portion_sum = round(sum([i.portion for i in portion]), 2)
    proteins_sum = round(sum([i.proteins for i in portion]), 2)
    carbs_sum = round(sum([i.carbs for i in portion]), 2)
    fats_sum = round(sum([i.fats for i in portion]), 2)

    return render_template('index.html', form=form, portion=portion, calories_sum=calories_sum,
                           portion_sum=portion_sum, proteins_sum=proteins_sum, carbs_sum=carbs_sum, fats_sum=fats_sum)


@bp.route('/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    id = Portion.query.filter_by(id=id).first_or_404()
    db.session.delete(id)
    db.session.commit()
    return redirect(url_for('food.index', time='today'))
