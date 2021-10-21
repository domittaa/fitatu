from werkzeug.security import generate_password_hash
from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegisterForm, EditProfileForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User


@app.route('/', methods=['GET'])
@login_required
def index():  # put application's code here
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash("You are now registered user. Please login.")
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@login_required
@app.route('/user/<id>', methods=['GET', 'POST'])
def profile_page(id):
    user = User.query.filter_by(id=id).first()
    return render_template('profile_page.html', user=user)


@login_required
@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.weight = form.weight.data
        current_user.height = form.height.data
        current_user.sex = form.sex.data
        current_user.age = form.age.data
        current_user.pal = form.pal.data
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for('profile_page', id=current_user.id))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.weight.data = current_user.weight
        form.height.data = current_user.height
        form.sex.data = current_user.sex
        form.age.data = current_user.age
        form.pal.data = current_user.pal

    return render_template('edit_profile.html', form=form)

