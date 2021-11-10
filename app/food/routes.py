from datetime import datetime, date
from flask import url_for, redirect, render_template, flash, request, current_app
from sqlalchemy import extract
from app.food import bp
from app import db
from app.models import Food, Portion
from app.food.forms import FoodForm, FoodTracker, DateForm, SearchForm
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
        calories = round(proteins*4 + fats*9 + carbs*4, 2)
        check_if_product_in_database = Food.query.filter_by(name=name).first()
        if check_if_product_in_database is None:
            add_product = Food(name=name, proteins=proteins, carbs=carbs, fats=fats, calories=calories)
            db.session.add(add_product)
            db.session.commit()
        else:
            flash(f'{check_if_product_in_database.name} already in database!')
        return redirect(url_for('food.add'))

    return render_template('food/add.html', form=form)


@bp.route('/products', methods=['GET', 'POST'])
@login_required
def products_info():
    page = request.args.get('page', 1, type=int)
    form = SearchForm()
    if form.validate_on_submit():
        name = form.name.data
        search = "%{}%".format(name)
        products = Food.query.filter(Food.name.like(search)).all()
        if products:
            return render_template('food/products_info.html', food=products, form=form)
        else:
            flash(f'Cant find {name} in our database.')

    products = Food.query.order_by('name').paginate(page, current_app.config['ITEMS_PER_PAGE'], False)
    next_url = url_for('food.products_info', page=products.next_num) if products.has_next else None
    prev_url = url_for('food.products_info', page=products.prev_num) if products.has_prev else None
    return render_template('food/products_info.html', food=products.items, next_url=next_url, prev_url=prev_url, form=form)


@bp.route('/tracker', defaults={'time': datetime.today().strftime('%Y-%m-%d')}, methods=['GET', 'POST'])
@bp.route('/tracker/<time>', methods=['GET', 'POST'])
@login_required
def tracker(time):
    form = FoodTracker()
    now = datetime.utcnow()
    if form.validate_on_submit():
        name = form.name.data.capitalize()
        portion = form.portion.data
        check = Food.query.filter_by(name=name).first()
        if check is None:
            flash(f'No {name} in our database. Use link below to add {name} to our database.')
            return redirect(url_for('food.tracker'))
        else:
            proteins = check.proteins*portion/100
            carbs = check.carbs*portion/100
            fats = check.fats*portion/100
            calories = check.calories*portion/100
            food = Portion(name=name, portion=portion, proteins=proteins, carbs=carbs, fats=fats, calories=calories,
                           user=current_user,
                           time=datetime.strptime(time, '%Y-%m-%d'))
            db.session.add(food)
            db.session.commit()

    date_form = DateForm()
    if date_form.validate_on_submit():
        time = date_form.date.data
        return redirect(url_for('food.tracker', time=time))
    portion = Portion.query.filter(extract('year', Portion.time) == time[:4],
                                   extract('month', Portion.time) == time[5:7],
                                   extract('day', Portion.time) == time[8:10]).filter_by(user_id=current_user.id).all()

    calories_sum = round(sum([i.calories for i in portion]), 2)
    portion_sum = round(sum([i.portion for i in portion]), 2)
    proteins_sum = round(sum([i.proteins for i in portion]), 2)
    carbs_sum = round(sum([i.carbs for i in portion]), 2)
    fats_sum = round(sum([i.fats for i in portion]), 2)

    return render_template('food/tracker.html', form=form, portion=portion, calories_sum=calories_sum, now=now,
                           portion_sum=portion_sum, proteins_sum=proteins_sum, carbs_sum=carbs_sum, fats_sum=fats_sum,
                           date_form=date_form, time=time)


def redirect_url(default='index'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)


@bp.route('/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    id = Portion.query.filter_by(id=id).first_or_404()
    db.session.delete(id)
    db.session.commit()
    return redirect(redirect_url())


