from flask import url_for, redirect, render_template, flash
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
        redirect(url_for('list.list'))
    return render_template('list/list.html', form=form, lists=lists)


