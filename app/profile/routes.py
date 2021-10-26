from collections import defaultdict

from sqlalchemy import extract

from app import db
from flask import current_app
from app.profile import bp
from flask import render_template, flash, redirect, url_for, request
from app.profile.profile import EditProfileForm
from flask_login import current_user, login_required
from app.models import User, Portion
import os
from werkzeug.utils import secure_filename
import imghdr
from matplotlib import pyplot as plt

import io
import base64


@login_required
@bp.route('/user/<id>', methods=['GET', 'POST'])
def profile_page(id):
    user = User.query.filter_by(id=id).first()
    portion = Portion.query.filter_by(user_id=user.id).all()
    d_calories = defaultdict(list)
    d_proteins = defaultdict(list)
    d_carbs = defaultdict(list)
    for i in portion:
        d_calories[i.time.strftime("%d/%m/%Y")].append(i.calories)
        d_proteins[i.time.strftime("%d/%m/%Y")].append(i.proteins)
        d_carbs[i.time.strftime("%d/%m/%Y")].append(i.carbs)

    calories = [sum(i) for i in d_calories.values()]
    proteins = [sum(i) for i in d_proteins.values()]
    carbs = [sum(i) for i in d_carbs.values()]


    days = list(d_calories.keys())

    def fig_to_base64(fig):
        img = io.BytesIO()
        fig.savefig(img, format='png',
                    bbox_inches='tight')
        img.seek(0)

        return base64.b64encode(img.getvalue())

    fig, ax = plt.subplots()
    plt.scatter(days, calories)
    plt.scatter(days, proteins)
    plt.scatter(days, carbs)
    plt.legend(['Calories', 'Proteins', 'Carbs'])
    encoded = fig_to_base64(fig)
    my_html = "data:image/png;base64, {}".format(encoded.decode('utf-8'))
    return render_template('profile/profile_page.html', user=user, my_html=my_html)


def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')


@login_required
@bp.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        uploaded_file = request.files['avatar']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in current_app.config['UPLOAD_EXTENSIONS'] or \
                    file_ext != validate_image(uploaded_file.stream):
                flash('Invalid image!')
                return redirect(url_for('edit_profile'))
            uploaded_file.save(os.path.join(current_app.config['UPLOAD_AVATAR_PATH'], str(current_user.id)))
        User.query.filter_by(id=current_user.id).update(
            {"avatar": (filename), "weight": (form.weight.data), "height": (form.height.data), "sex": (form.sex.data),
             "age": (form.age.data), "pal": (form.pal.data)})
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for('profile.profile_page', id=current_user.id))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.weight.data = current_user.weight
        form.height.data = current_user.height
        form.sex.data = current_user.sex
        form.age.data = current_user.age
        form.pal.data = current_user.pal

    return render_template('profile/edit_profile.html', form=form)




