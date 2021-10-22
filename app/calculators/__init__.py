from flask import Blueprint

bp = Blueprint('calculators', __name__)

from app.calculators import routes