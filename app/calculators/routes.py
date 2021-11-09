from flask import render_template, flash
from flask_login import login_required
from app.calculators import bp
from app.calculators.forms import BMIForm, BMRForm, TERForm


@bp.route('/bmi', methods=['GET', 'POST'])
@login_required
def bmi():
    form = BMIForm()
    if form.validate_on_submit():
        weight = form.weight.data
        height = form.height.data
        bmi = round(weight/height**2,1)
        flash(f"Your BMI is {bmi}. Check the table below for more informations.")
    return render_template('calculators/bmi.html', form=form)


@bp.route('/bmr', methods=['GET', 'POST'])
@login_required
def bmr():
    form = BMRForm()
    if form.validate_on_submit():
        weight = form.weight.data
        height = form.height.data
        age = form.age.data
        sex = form.sex.data
        if sex == "Female":
            bmr = round(655.1 + 9.563*weight + 1.85*height - 4.676*age,2)
        else:
            bmr = round(66.5 + 13.75*weight + 5.003*height - 6.775*age, 2)
        flash(f"Your BMR is {bmr} calories per day.")
    return render_template('calculators/bmr.html', form=form)


@bp.route('/ter', methods=['GET', 'POST'])
@login_required
def ter():
    form = TERForm()
    if form.validate_on_submit():
        weight = form.weight.data
        height = form.height.data
        age = form.age.data
        sex = form.sex.data
        pal = float(form.pal.data)
        if sex == "Female":
            ter = round((655.1 + 9.563*weight + 1.85*height - 4.676*age)*pal, 2)
        else:
            ter = round((66.5 + 13.75*weight + 5.003*height - 6.775*age)*pal, 2)
        flash(f"Your TER is {ter} calories per day.")
    return render_template('calculators/ter.html', form=form)
