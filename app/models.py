from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    weight = db.Column(db.Integer)
    height = db.Column(db.Integer)
    sex = db.Column(db.String(64))
    age = db.Column(db.Integer)
    pal = db.Column(db.Integer)
    avatar = db.Column(db.String(240))
    portions = db.relationship('Portion', backref='user', lazy='dynamic')
    list = db.relationship('List', backref='user', lazy='dynamic')
    fridge = db.relationship('Fridge', backref='user', lazy='dynamic')
    menu = db.relationship('Menu', backref='user', lazy='dynamic')
    workout = db.relationship('Workout', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    proteins = db.Column(db.Integer, nullable=False)
    carbs = db.Column(db.Integer, nullable=False)
    fats = db.Column(db.Integer, nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    fridge = db.relationship('Fridge', backref='product', lazy='dynamic')


class Portion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    portion = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)
    proteins = db.Column(db.Integer, nullable=False)
    carbs = db.Column(db.Integer, nullable=False)
    fats = db.Column(db.Integer, nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    time = db.Column(db.DateTime, index=True, default=datetime.utcnow)


class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    products = db.relationship('ListProduct', backref='list', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class ListProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer)
    status = db.Column(db.Boolean)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'))


class Fridge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer)
    expired_date = db.Column(db.Date)
    category = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'))


class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    products = db.Column(db.String)
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category = db.Column(db.String)


class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String)
    description = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.Date)




