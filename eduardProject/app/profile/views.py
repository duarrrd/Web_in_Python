from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from . import profile_bp
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, UpdateAccountForm
from .models import User
from app import db
import os
import shutil
from datetime import datetime

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

@profile_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('cookies.info'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.checkPassword(form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Login successful", category="success")
            return redirect(url_for("cookies.info"))

        flash("Invalid email or password", category="danger")
        return redirect(url_for("profile.login"))

    return render_template('profile/login.html', form=form)

@profile_bp.route('/registration', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('cookies.info'))

    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash(f"Account created for {new_user.username}!", "success")
            return redirect(url_for("profile.login"))
        except:
            db.session.rollback()
            flash("ERROR, try using different data", category="danger")
            return redirect(url_for("profile.registration"))

    return render_template("profile/register.html", form=form)

@profile_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST' or request.method == 'GET':
        logout_user()
        flash("You've been logged out", category="success")
        return redirect(url_for("profile.login"))
    return redirect(url_for("profile.login"))

@profile_bp.route('/change_password', methods=['POST'])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        user = current_user

        if user and user.checkPassword(form.old_password.data):
            try:
                # Update the password
                user.set_password(form.new_password.data)
                db.session.commit()
                flash("Password changed", category="success")
            except Exception as e:
                db.session.rollback()
                flash(f"Error: {e}", category="danger")
        else:
            flash("Invalid password", category="danger")
    else:
        flash("Form validation failed", category="danger")

    return redirect(url_for('profile.account'))

@profile_bp.route('/users')
def users():
    return render_template('profile/users.html', users=User.query.all())

@profile_bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    UPLOAD_FOLDER = 'static/imgs/'

    # Use app context to set configuration value
    with current_app.app_context():
        current_app.config['upload_folder'] = UPLOAD_FOLDER

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    update_account_form = UpdateAccountForm(obj=current_user)
    change_password_form = ChangePasswordForm()

    if update_account_form.validate_on_submit():
        current_user.username = update_account_form.username.data
        current_user.email = update_account_form.email.data
        current_user.about_me = update_account_form.about_me.data

        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                filename = secure_filename(file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                current_user.image_file = filename

                # Move the file to the UPLOAD_FOLDER
                destination = os.path.join(current_app.root_path, UPLOAD_FOLDER, filename)
                if not os.path.exists(os.path.join(current_app.root_path, UPLOAD_FOLDER)):
                    os.makedirs(os.path.join(current_app.root_path, UPLOAD_FOLDER))
                file.save(destination)

        db.session.commit()
        flash('Account updated successfully!', 'success')
        return redirect(url_for('profile.account'))

    if change_password_form.validate_on_submit():
        if current_user.check_password(change_password_form.old_password.data):
            try:
                current_user.set_password(change_password_form.new_password.data)
                db.session.commit()
                flash('Password changed successfully!', 'success')
                return redirect(url_for('profile.account'))
            except Exception as e:
                db.session.rollback()
                flash(f"Error changing password: {e}", 'danger')
        else:
            flash('Current password is incorrect', 'danger')

    return render_template('profile/account.html', update_account_form=update_account_form, change_password_form=change_password_form, is_authenticated=True, os=os)
@profile_bp.before_request
def update_last_seen():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
