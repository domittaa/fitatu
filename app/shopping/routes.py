from datetime import datetime

from flask import url_for, redirect, render_template, flash
from sqlalchemy import desc
from app.shopping import bp
from app import db
from app.models import List, ListProduct, Fridge
from flask_login import login_required, current_user
from app.shopping.forms import ListForm, ListProductForm, FridgeForm


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
