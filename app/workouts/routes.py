from datetime import datetime, date, timedelta
from flask import url_for, redirect, render_template, request

from app.food.routes import redirect_url
from app.week_func import get_week
from app.workouts import bp
from app import db
from app.models import List, ListProduct, Fridge, Menu, Workout
from flask_login import login_required, current_user
from app.workouts.forms import WorkoutForm


@bp.route('/workout_plan', defaults={'date': str(date.today())}, methods=['GET', 'POST'])
@bp.route('/workout_plan/<date>', methods = ['GET', 'PUT'])
@login_required
def workout_plan(date):
    today = datetime.strptime(date, '%Y-%m-%d').date()
    tomorrow = today + timedelta(days=7)
    yesterday = today - timedelta(days=7)
    week = get_week(date)

    monday_plan = Workout.query.filter_by(user=current_user, date=week['monday']).all()
    tuesday_plan = Workout.query.filter_by(user=current_user, date=week['tuesday']).all()
    wednesday_plan = Workout.query.filter_by(user=current_user, date=week['wednesday']).all()
    thursday_plan = Workout.query.filter_by(user=current_user, date=week['thursday']).all()
    friday_plan = Workout.query.filter_by(user=current_user, date=week['friday']).all()
    saturday_plan = Workout.query.filter_by(user=current_user, date=week['saturday']).all()
    sunday_plan = Workout.query.filter_by(user=current_user, date=week['sunday']).all()

    plan = [monday_plan, tuesday_plan, wednesday_plan, thursday_plan, friday_plan, saturday_plan, sunday_plan]

    return render_template('workouts/workout_plan.html', today=today, tomorrow=tomorrow, yesterday=yesterday, week=week,
                           monday_plan=monday_plan, tuesday_plan=tuesday_plan, wednesday_plan=wednesday_plan,
                           thursday_plan=thursday_plan, friday_plan=friday_plan, saturday_plan=saturday_plan,
                           sunday_plan=sunday_plan, plan=plan)


@bp.route('/add_workout/<date>', methods=['GET', 'POST'])
@login_required
def add_workout(date):
    form = WorkoutForm()
    if form.validate_on_submit():
        new_workout = Workout(category=form.category.data, description=form.description.data,
                              user=current_user, date=datetime.strptime(date, '%Y-%m-%d').date())
        db.session.add(new_workout)
        db.session.commit()
        return redirect(url_for('workouts.workout_plan', date=date))
    return render_template('workouts/add_workout.html', form=form, date=date)


@bp.route('/delete_workout/<id>', methods=['GET', "POST"])
@login_required
def delete_workout(id):
    workout_to_delete = Workout.query.filter_by(id=id).first()
    db.session.delete(workout_to_delete)
    db.session.commit()
    return redirect(url_for('workouts.workout_plan', date=workout_to_delete.date))
