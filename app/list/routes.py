from flask import url_for, redirect, render_template, flash
from sqlalchemy import desc

from app.list import bp
from app import db
from app.models import List, ListProduct
from flask_login import login_required, current_user
from app.list.forms import ListForm, ListProductForm


@login_required
@bp.route('/list', methods=['GET', 'POST'])
def list():
    lists = List.query.filter_by(user_id=current_user.id).all()
    form = ListForm()
    if form.validate_on_submit():
        list = List(name=form.name.data,user_id=current_user.id)
        db.session.add(list)
        db.session.commit()
        return redirect(url_for('list.list'))
    return render_template('list/list.html', form=form, lists=lists)


@login_required
@bp.route('/list/<id>', methods=['GET', 'POST'])
def view_list(id):
    list = List.query.filter_by(id=id).first_or_404()
    form = ListProductForm()
    if form.validate_on_submit():
        new_product = ListProduct(name=form.name.data, quantity=form.quantity.data, list_id=id, status=True)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('list.view_list', id=list.id))
    products = ListProduct.query.filter_by(list_id=id).order_by(desc('status'))
    return render_template('list/view_list.html', products=products, form=form, list=list)


@login_required
@bp.route('/delete/product/<id>', methods=['GET', 'POST'])
def delete_product(id):
    product = ListProduct.query.filter_by(id=id).first_or_404()
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('list.view_list', id=product.list_id))


@login_required
@bp.route('/bought/product/<id>', methods=['GET', 'POST'])
def move_to_bought(id):
    product = ListProduct.query.filter_by(id=id).first_or_404()
    if product.status:
        product.status = False
        db.session.commit()
    else:
        product.status = True
        db.session.commit()
    return redirect(url_for('list.view_list', id=product.list_id))


@login_required
@bp.route('/delete/list/<id>', methods=['GET', 'POST'])
def delete_list(id):
    list = List.query.filter_by(id=id).first_or_404()
    db.session.delete(list)
    db.session.commit()
    return redirect(url_for('list.list', id=id))


