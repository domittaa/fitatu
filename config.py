import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_AVATAR_PATH = 'app/static/avatars'
    UPLOAD_EXTENSIONS = ['.jpg', '.png', '.gif']
    ITEMS_PER_PAGE = 5
    MAX_CONTENT_LENGTH = 1024 * 1024
