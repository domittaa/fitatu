from datetime import datetime, date, timedelta
from flask import url_for, redirect, render_template
from sqlalchemy import desc
from app.shopping import bp
from app import db
from app.models import List, ListProduct, Fridge, Menu
from flask_login import login_required, current_user
from app.shopping.forms import ListForm, ListProductForm, FridgeForm, MenuForm


@bp.route('/list ', methods=['GET', 'POST'])
@login_required
def list():
    lists = List.query.filter_by(user=current_user).all()
    form = ListForm()
    if form.validate_on_submit():
        list = List(name=form.name.data, user=current_user)
        db.session.add(list)
        db.session.commit()
        return redirect(url_for('shopping.shopping'))
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


@bp.route('/week_menu', methods=['GET', 'POST'])
@login_required
def week_menu():
    today = date.today()

    week = []

    if today.weekday() == 0:
        monday = today
        tuesday = today + timedelta(days=1)
        wednesday = today + timedelta(days=2)
        thursday = today + timedelta(days=3)
        friday = today + timedelta(days=4)
        saturday = today + timedelta(days=5)
        sunday = today + timedelta(days=6)

        week = [i for i in (monday, tuesday, wednesday, thursday, friday, saturday, sunday)]

    elif today.weekday() == 1:
        tuesday = today
        monday = today - timedelta(days=1)
        wednesday = today + timedelta(days=1)
        thursday = today + timedelta(days=2)
        friday = today + timedelta(days=3)
        saturday = today + timedelta(days=4)
        sunday = today + timedelta(days=5)

        week = {key: value for (key, value) in (
            ('monday', monday), ('tuesday', tuesday),  ('wednesday', wednesday), ('thursday', thursday),
            ('friday', friday), ('saturday', saturday), ('sunday', sunday))}

    elif today.weekday() == 2:
        wednesday = today
        monday = today - timedelta(days=2)
        tuesday = today - timedelta(days=1)
        thursday = today + timedelta(days=1)
        friday = today + timedelta(days=2)
        saturday = today + timedelta(days=3)
        sunday = saturday + timedelta(days=4)

        week = {key: value for (key, value) in (
            ('monday', monday), ('tuesday', tuesday),  ('wednesday', wednesday), ('thursday', thursday),
            ('friday', friday), ('saturday', saturday), ('sunday', sunday))}

    elif today.weekday() == 3:
        thursday = today
        monday = today - timedelta(days=3)
        tuesday = today - timedelta(days=2)
        wednesday = today - timedelta(days=1)
        friday = today + timedelta(days=1)
        saturday = today + timedelta(days=2)
        sunday = saturday + timedelta(days=3)

        week = {key: value for (key, value) in (
            ('monday', monday), ('tuesday', tuesday),  ('wednesday', wednesday), ('thursday', thursday),
            ('friday', friday), ('saturday', saturday), ('sunday', sunday))}

    elif today.weekday() == 4:
        friday = today
        monday = today - timedelta(days=4)
        tuesday = today - timedelta(days=3)
        wednesday = today - timedelta(days=2)
        thursday = today - timedelta(days=1)
        saturday = today + timedelta(days=1)
        sunday = today + timedelta(days=2)

        week = {key: value for (key, value) in (
            ('monday', monday), ('tuesday', tuesday),  ('wednesday', wednesday), ('thursday', thursday),
            ('friday', friday), ('saturday', saturday), ('sunday', sunday))}

    elif today.weekday() == 5:
        saturday = today
        monday = today - timedelta(days=5)
        tuesday = today - timedelta(days=4)
        wednesday = today - timedelta(days=3)
        thursday = today - timedelta(days=2)
        friday = today - timedelta(days=1)
        sunday = today + timedelta(days=1)

        week = {key: value for (key, value) in (
            ('monday', monday), ('tuesday', tuesday),  ('wednesday', wednesday), ('thursday', thursday),
            ('friday', friday), ('saturday', saturday), ('sunday', sunday))}

    elif today.weekday() == 6:
        sunday = today
        monday = today - timedelta(days=6)
        tuesday = today - timedelta(days=5)
        wednesday = today - timedelta(days=4)
        thursday = today - timedelta(days=3)
        friday = today - timedelta(days=3)
        saturday = today - timedelta(days=1)

        week = {key: value for (key, value) in (
            ('monday', monday), ('tuesday', tuesday),  ('wednesday', wednesday), ('thursday', thursday),
            ('friday', friday), ('saturday', saturday), ('sunday', sunday))}

    menu_monday = Menu.query.filter_by(date=week['monday']).all()
    menu_tuesday = Menu.query.filter_by(date=week['tuesday']).all()
    menu_wednesday = Menu.query.filter_by(date=week['wednesday']).all()
    menu_thursday = Menu.query.filter_by(date=week['thursday']).all()
    menu_friday = Menu.query.filter_by(date=week['friday']).all()
    menu_sunday = Menu.query.filter_by(date=week['sunday']).all()
    menu_saturday = Menu.query.filter_by(date=week['saturday']).all()

    return render_template('shopping/week_menu.html', menu_monday=menu_monday, menu_tuesday=menu_tuesday,
                           menu_wednesday=menu_wednesday, menu_thursday=menu_thursday, menu_friday=menu_friday,
                           menu_saturday=menu_saturday, menu_sunday=menu_sunday, week=week)


@bp.route('/daily_menu/<day>', methods=['GET', 'POST'])
@login_required
def daily_menu(day):
    form = MenuForm()
    if form.validate_on_submit():
        name = form.name.data
        products = form.products.data
        category = form.category.data
        # calories_sum = 0
        # for product in products:
        #     calories = Portion.query.with_entities(Portion.calories).filter(Portion.name == product).first()
        #     if calories:
        #         calories_sum += calories
        #     else:
        #         flash(f'{product} not in database')
        dish = Menu(name=name, products=products, date=datetime.strptime(day, '%Y-%m-%d').date(),
                    category=category, user=current_user)

        db.session.add(dish)
        db.session.commit()
        return redirect(url_for('shopping.daily_menu', day=dish.date))
    dishes = Menu.query.filter_by(date=day).all()
    date = day
    return render_template('shopping/daily_menu.html', form=form, dishes=dishes, date=date)
