from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
bootstrap = Bootstrap()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login.init_app(app)
    login.login_view = 'auth.login'
    bootstrap.init_app(app)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.calculators import bp as calculators_bp
    app.register_blueprint(calculators_bp)

    from app.profile import bp as profile_bp
    app.register_blueprint(profile_bp)

    from app.food import bp as food_bp
    app.register_blueprint(food_bp)

    from app.shopping import bp as shopping_bp
    app.register_blueprint(shopping_bp)

    return app

from app import models
