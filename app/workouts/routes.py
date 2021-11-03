from datetime import datetime, date, timedelta
from flask import url_for, redirect, render_template
from app.week_func import get_week
from app.workouts import bp
from app import db
from app.models import List, ListProduct, Fridge, Menu
from flask_login import login_required, current_user
from app.shopping.forms import ListForm, ListProductForm, FridgeForm, MenuForm


@bp.route('/workout_plan', defaults={'date': str(date.today())}, methods=['GET', 'POST'])
@bp.route('/workout_plan/<date>', methods = ['GET', 'PUT'])
@login_required
def workout_plan(date):
    today = datetime.strptime(date, '%Y-%m-%d').date()
    tomorrow = today + timedelta(days=7)
    yesterday = today - timedelta(days=7)
    week = get_week(date)

    return render_template('workouts/workout_plan.html', today=today, tomorrow=tomorrow, yesterday=yesterday, week=week)