from collections import defaultdict
from datetime import datetime, date, timedelta
from flask import url_for, redirect, render_template
from sqlalchemy import desc
from app.shopping import bp
from app import db
from app.models import List, ListProduct, Fridge, Menu
from flask_login import login_required, current_user
from app.shopping.forms import ListForm, ListProductForm, FridgeForm, MenuForm
from app.week_func import get_week
from app.food.routes import redirect_url



@bp.route('/list ', methods=['GET', 'POST'])
@login_required
def list():
    lists = List.query.filter_by(user=current_user).all()
    form = ListForm()
    if form.validate_on_submit():
        list = List(name=form.name.data, user=current_user)
        db.session.add(list)
        db.session.commit()
        return redirect(url_for('shopping.list'))
    return render_template('shopping/list.html', form=form, lists=lists)


@bp.route('/list/<id>', methods=['GET', 'POST'])
@login_required
def view_list(id):
    list = List.query.filter_by(id=id).first_or_404()
    form = ListProductForm()
    if form.validate_on_submit():
        new_product = ListProduct(name=form.name.data.capitalize(), quantity=form.quantity.data, list=list, status=True)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('shopping.view_list', id=list.id))
    products = ListProduct.query.filter_by(list_id=id).order_by(desc('status'))
    return render_template('shopping/view_list.html', products=products, form=form, list=list)


@bp.route('/delete/product/<id>', methods=['GET', 'POST'])
@login_required
def delete_product(id):
    product = ListProduct.query.filter_by(id=id).first_or_404()
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('shopping.view_list', id=product.list_id))


@bp.route('/bought/product/<id>', methods=['GET', 'POST'])
@login_required
def move_to_bought(id):
    product = ListProduct.query.filter_by(id=id).first_or_404()
    if product.status:
        product.status = False
        db.session.commit()
    else:
        product.status = True
        db.session.commit()
    return redirect(url_for('shopping.view_list', id=product.list_id))


@bp.route('/delete/list/<id>', methods=['GET', 'POST'])
@login_required
def delete_list(id):
    list = List.query.filter_by(id=id).first_or_404()
    db.session.delete(list)
    db.session.commit()
    return redirect(url_for('shopping.list', id=id))


@bp.route('/fridge', methods=['GET', 'POST'])
@login_required
def fridge():
    form = FridgeForm()
    now = datetime.today().date()
    if form.validate_on_submit():
        product = Fridge(name=form.name.data.capitalize(), quantity=form.quantity.data,
                         expired_date=form.expired_date.data, category=form.category.data, user=current_user)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('shopping.fridge'))
    products = Fridge.query.filter_by(user=current_user).order_by('expired_date').all()
    return render_template('shopping/fridge.html', form=form, products=products, now=now)


@bp.route('/delete/fridge_product/<id>', methods=['GET', 'POST'])
@login_required
def delete_product_from_fridge(id):
    product = Fridge.query.filter_by(id=id).first_or_404()
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('shopping.fridge'))


@bp.route('/week_menu', defaults={'date': str(date.today())}, methods=['GET', 'POST'])
@bp.route('/week_menu/<date>', methods=['GET', 'POST'])
@login_required
def week_menu(date):
    today = datetime.strptime(date, '%Y-%m-%d').date()
    tomorrow = today + timedelta(days=7)
    yesterday = today - timedelta(days=7)

    week = get_week(date)

    menu_monday = Menu.query.filter_by(date=week['monday']).all()
    menu_tuesday = Menu.query.filter_by(date=week['tuesday']).all()
    menu_wednesday = Menu.query.filter_by(date=week['wednesday']).all()
    menu_thursday = Menu.query.filter_by(date=week['thursday']).all()
    menu_friday = Menu.query.filter_by(date=week['friday']).all()
    menu_sunday = Menu.query.filter_by(date=week['sunday']).all()
    menu_saturday = Menu.query.filter_by(date=week['saturday']).all()

    return render_template('shopping/week_menu.html', menu_monday=menu_monday, menu_tuesday=menu_tuesday,
                           menu_wednesday=menu_wednesday, menu_thursday=menu_thursday, menu_friday=menu_friday,
                           menu_saturday=menu_saturday, menu_sunday=menu_sunday, week=week,
                           today=today, yesterday=yesterday, tomorrow=tomorrow)


@bp.route('/daily_menu/<day>', methods=['GET', 'POST'])
@login_required
def daily_menu(day):
    date = day

    form = MenuForm()
    if form.validate_on_submit():
        name = form.name.data
        products = form.products.data
        category = form.category.data
        dish = Menu(name=name, products=products, date=datetime.strptime(day, '%Y-%m-%d').date(),
                    category=category, user=current_user)
        db.session.add(dish)
        db.session.commit()
        return redirect(url_for('shopping.daily_menu', day=dish.date))

    dishes = Menu.query.filter_by(date=day).all()

    in_fridge = defaultdict(list, {k: [] for k in ('Breakfast', 'Second breakfast', 'Lunch', 'Dessert', 'Dinner')})
    must_buy = defaultdict(list, {k: [] for k in ('Breakfast', 'Second breakfast', 'Lunch', 'Dessert', 'Dinner')})

    for dish in dishes:
        for product in dish.products.split(','):
            check_fridge = Fridge.query.filter_by(name=product.capitalize(), user=current_user).all()
            if check_fridge:
                in_fridge[dish.category].append(product)
            else:
                must_buy[dish.category].append(product)
    return render_template('shopping/daily_menu.html', form=form, dishes=dishes, date=date, in_fridge=in_fridge,
                           must_buy=must_buy)


@bp.route('/delete/menu/<id>', methods=['GET', "POST"])
@login_required
def delete_menu(id):
    id = Menu.query.filter_by(id=id).first()
    db.session.delete(id)
    db.session.commit()
    return redirect(redirect_url())