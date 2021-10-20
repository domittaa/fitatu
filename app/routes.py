from app import app
from flask import render_template
from app.forms import LoginForm


@app.route('/', methods=['GET'])
def hello_world():  # put application's code here
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)