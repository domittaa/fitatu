from werkzeug.security import generate_password_hash
from app import app, db
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm, RegisterForm
from app.models import User


@app.route('/', methods=['GET'])
def hello_world():  # put application's code here
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data,
                        password_hash=generate_password_hash(form.password.data, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        flash("You are now registered user. Please login.")
        return redirect(url_for('login'))

    return render_template('register.html', form=form)
