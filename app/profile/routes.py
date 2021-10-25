from app import db
from flask import current_app
from app.profile import bp
from flask import render_template, flash, redirect, url_for, request
from app.profile.profile import EditProfileForm
from flask_login import current_user, login_required
from app.models import User
import os
from werkzeug.utils import secure_filename
import imghdr


@login_required
@bp.route('/user/<id>', methods=['GET', 'POST'])
def profile_page(id):
    user = User.query.filter_by(id=id).first()
    return render_template('profile/profile_page.html', user=user)


def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')


@login_required
@bp.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        uploaded_file = request.files['avatar']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in current_app.config['UPLOAD_EXTENSIONS'] or \
                    file_ext != validate_image(uploaded_file.stream):
                flash('Invalid image!')
                return redirect(url_for('edit_profile'))
            uploaded_file.save(os.path.join(current_app.config['UPLOAD_AVATAR_PATH'], str(current_user.id)))
        User.query.filter_by(id=current_user.id).update(
            {"avatar": (filename), "weight": (form.weight.data), "height": (form.height.data), "sex": (form.sex.data),
             "age": (form.age.data), "pal": (form.pal.data)})
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for('profile.profile_page', id=current_user.id))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.weight.data = current_user.weight
        form.height.data = current_user.height
        form.sex.data = current_user.sex
        form.age.data = current_user.age
        form.pal.data = current_user.pal

    return render_template('profile/edit_profile.html', form=form)




