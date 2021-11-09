from datetime import datetime
from collections import defaultdict
from sqlalchemy import extract
from app import db
from flask import current_app
from app.profile import bp
from flask import render_template, flash, redirect, url_for, request
from app.profile.forms import EditProfileForm, SelectDateForm
from flask_login import current_user, login_required
from app.models import User, Portion
import os
from werkzeug.utils import secure_filename
import imghdr
from matplotlib import pyplot as plt
import random
import io
import base64


@login_required
@bp.route('/', methods=['GET', 'POST'])
def index():
    quotes_path = os.path.join(current_app.config['TEXT_PATH'], 'quotes.txt')
    open_quotes = open(quotes_path)
    quotes = open_quotes.readlines()
    quote = random.choice(quotes)

    tips_path = os.path.join(current_app.config['TEXT_PATH'], 'tips.txt')
    open_tips = open(tips_path, encoding='utf8')
    tips = open_tips.readlines()
    tip = random.choice(tips)
    tip_header = tip.split(':')[0]
    tip_body = tip.split(':')[1]

    return render_template('profile/index.html', quote=quote, tip_header=tip_header, tip_body=tip_body)


def fig_to_base64(fig):
    img = io.BytesIO()
    fig.savefig(img, format='png',
                bbox_inches='tight')
    img.seek(0)

    return base64.b64encode(img.getvalue())


@login_required
@bp.route('/user/<id>', methods=['GET', 'POST'])
def profile_page(id):
    user = User.query.filter_by(id=id).first()
    form = SelectDateForm()
    form.month.choices = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
                          'October', 'November', 'December']
    form.year.choices = ['2021', '2022', '2023']
    months = {'January': 1, 'February': 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8,
              "September": 9, "October": 10, "November": 11, "December": 12}

    d_calories = defaultdict(list)
    d_proteins = defaultdict(list)
    d_carbs = defaultdict(list)
    d_fats = defaultdict(list)

    if form.validate_on_submit():
        month = months[form.month.data]
        year = form.year.data

        portion = Portion.query.filter(extract('month', Portion.time) == month, extract('year', Portion.time) == year,
                                       Portion.user_id == user.id).order_by(Portion.time).all()
        for i in portion:
            d_calories[i.time.strftime("%d/%m/%Y")].append(i.calories)
            d_proteins[i.time.strftime("%d/%m/%Y")].append(i.proteins)
            d_carbs[i.time.strftime("%d/%m/%Y")].append(i.carbs)
            d_fats[i.time.strftime("%d/%m/%Y")].append(i.fats)

    elif request.method == "GET":
        month = datetime.utcnow().month
        year = datetime.utcnow().year

        portion = Portion.query.filter(extract('month', Portion.time) == month, extract('year', Portion.time) == year,
                                       Portion.user_id == user.id).order_by(Portion.time).all()
        for i in portion:
            d_calories[i.time.strftime("%d/%m/%Y")].append(i.calories)
            d_proteins[i.time.strftime("%d/%m/%Y")].append(i.proteins)
            d_carbs[i.time.strftime("%d/%m/%Y")].append(i.carbs)
            d_fats[i.time.strftime("%d/%m/%Y")].append(i.fats)

    calories = [sum(i) for i in d_calories.values()]
    proteins = [sum(i) for i in d_proteins.values()]
    carbs = [sum(i) for i in d_carbs.values()]
    fats = [sum(i) for i in d_fats.values()]
    days = list(d_calories.keys())

    calories_fig, ax = plt.subplots()
    plt.scatter(days, calories, c="thistle")
    plt.xticks(days, rotation='vertical')
    plt.legend(['Calories'])
    plt.ylabel('calories')
    nutrition_fig, ax2 = plt.subplots()
    plt.scatter(days, proteins, c='pink')
    plt.scatter(days, carbs, c='mediumpurple')
    plt.scatter(days, fats, c='cadetblue')
    plt.ylabel('grams')
    plt.xticks(days, rotation='vertical')
    plt.legend(['Proteins', 'Carbs', 'Fats'])
    encoded_calories = fig_to_base64(calories_fig)
    encoded_nutritions = fig_to_base64(nutrition_fig)

    calories_plot = "data:image/png;base64, {}".format(encoded_calories.decode('utf-8'))
    nutrition_plot = "data:image/png;base64, {}".format(encoded_nutritions.decode('utf-8'))

    return render_template('profile/profile_page.html', user=user, calories_plot=calories_plot,
                           nutrition_plot=nutrition_plot, form=form)


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
    files = os.listdir(current_app.config['UPLOAD_AVATAR_PATH'])
    if form.validate_on_submit():
        uploaded_file = request.files['avatar']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in current_app.config['UPLOAD_EXTENSIONS'] or \
                    file_ext != validate_image(uploaded_file.stream):
                flash('Invalid image!')
                return redirect(url_for('profile.edit_profile'))
            uploaded_file.save(os.path.join(current_app.config['UPLOAD_AVATAR_PATH'], str(current_user.id)))
            User.query.filter_by(id=current_user.id).update({"avatar": (filename)})
        current_user.username = form.username.data
        current_user.weight = form.weight.data
        current_user.height = form.height.data
        current_user.sex = form.sex.data
        current_user.age = form.age.data
        current_user.pal = form.pal.data
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
        form.avatar.data = current_user.avatar

    return render_template('profile/edit_profile.html', form=form, files=files)




