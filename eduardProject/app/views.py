from flask import render_template, request, session, redirect, url_for, flash, make_response
from app import app, db
from datetime import datetime
import os
import json
from werkzeug.utils import secure_filename
from app.form import LoginForm, ChangePasswordForm, FeedbackForm, TodoForm, RegistrationForm, UpdateAccountForm
from app.models import Feedback, Todo, User
from flask_login import login_user, current_user, logout_user, login_required
import shutil

my_skills = ["Python","HTML","CSS","JS",]

user_session = {}

script_dir = os.path.dirname(os.path.realpath(__file__))
data_json_path = os.path.join(script_dir, 'data.json')

@app.route('/')
def main():
    OS = os.environ['OS']
    u_agent = request.user_agent
    time = datetime.now().strftime("%H:%M")
    return render_template('main.html', u_agent=u_agent, time=time, OS=OS)

@app.route('/l_and_s')
def l_and_s():
    return render_template('L&S.html')

@app.route('/skills/<int:id>')
@app.route('/skills')
def skills(id=None):
    if id is not None:
        if id > len(my_skills):
            abort(404)
        else:
            index = id - 1
            skill = my_skills[index]
            return render_template('skill.html', skill=skill)
    else:
        return render_template('skills.html', my_skills=my_skills)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('info'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.checkPassword(form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Login successful", category="success")
            return redirect(url_for("info"))

        flash("Invalid email or password", category="danger")
        return redirect(url_for("login"))

    return render_template('login.html', form=form)

@app.route("/registration", methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('info'))

    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash(f"Account created for {new_user.username}!", "success")
            return redirect(url_for("login"))
        except:
            db.session.rollback()
            flash("ERROR, try use another data", category="danger")
            return redirect(url_for("registration"))

    return render_template("register.html", form=form)

@app.route('/info', methods=['GET', 'POST'])
@login_required
def info():
    form = ChangePasswordForm()
    if current_user.is_authenticated:
        email = session['email']

        cookies = []
        for key, value in request.cookies.items():
            expiration = request.cookies[key]
            creation_time = session.get(f'cookie_creation_{key}')
            cookies.append({
                'key': key,
                'value': value,
                'expiration': expiration,
                'creation_time': creation_time,
            })

        if request.method == 'POST':
            if 'cookie_key' in request.form and 'cookie_value' in request.form and 'cookie_expiration' in request.form:
                cookie_key = request.form['cookie_key']
                cookie_value = request.form['cookie_value']
                cookie_expiration = int(request.form['cookie_expiration'])

                response = make_response(redirect(url_for('info')))
                response.set_cookie(cookie_key, cookie_value, max_age=cookie_expiration)
                session[f'cookie_creation_{cookie_key}'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                flash(f"Cookie '{cookie_key}' added successfully.", 'success')

            if 'delete_cookie_key' in request.form:
                delete_cookie_key = request.form['delete_cookie_key']

                if delete_cookie_key in request.cookies:
                    response = make_response(redirect(url_for('info')))
                    response.delete_cookie(delete_cookie_key)
                    session.pop(f'cookie_creation_{delete_cookie_key}', None)
                    flash(f"Cookie '{delete_cookie_key}' deleted successfully.", 'success')

            if 'delete_all_cookies' in request.form:
                response = make_response(redirect(url_for('info')))
                for key in request.cookies:
                    response.delete_cookie(key)
                    session.pop(f'cookie_creation_{key}', None)
                flash("All cookies deleted successfully.", 'success')

            return response

        return render_template('info.html', email=current_user.email, cookies=cookies, form=form)
    else:
        flash("You are not logged in. Please log in to access this page.", "error")
        return redirect(url_for('login'))

@app.route('/add_cookie', methods=['POST'])
def add_cookie():
    if 'username' in user_session:
        if request.method == 'POST':
            cookie_key = request.form.get('cookie_key')
            cookie_value = request.form.get('cookie_value')
            cookie_expiration = int(request.form.get('cookie_expiration'))

            response = make_response(redirect(url_for('info')))
            response.set_cookie(cookie_key, cookie_value, max_age=cookie_expiration)
            session[f'cookie_creation_{cookie_key}'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            flash(f"Cookie '{cookie_key}' added successfully.", 'success')

            return response
        else:
            return redirect(url_for('info'))
    else:
        return redirect(url_for('login'))

@app.route('/delete_cookie', methods=['POST'])
def delete_cookie():
    if 'username' in user_session:
        if request.method == 'POST':
            if 'delete_cookie_key' in request.form:
                delete_cookie_key = request.form['delete_cookie_key']

                if delete_cookie_key in request.cookies:
                    response = make_response(redirect(url_for('info')))
                    response.delete_cookie(delete_cookie_key)
                    session.pop(f'cookie_creation_{delete_cookie_key}', None)
                    flash(f"Cookie '{delete_cookie_key}' deleted successfully.", 'success')

                    return response

        return redirect(url_for('info'))
    else:
        return redirect(url_for('login'))

@app.route('/delete_all_cookies', methods=['POST'])
def delete_all_cookies():
    if 'username' in user_session:
        if request.method == 'POST':
            response = make_response(redirect(url_for('info')))
            for key in request.cookies:
                response.delete_cookie(key)
                session.pop(f'cookie_creation_{key}', None)
            flash("All cookies deleted successfully.", 'success')

            return response
        return redirect(url_for('info'))
    else:
        return redirect(url_for('login'))


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST' or request.method == 'GET':
        logout_user()
        flash("You've been logged out", category="success")
        return redirect(url_for("login"))
    return redirect(url_for("login"))

@app.route('/change_password', methods=['POST'])
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

    return redirect(url_for('account'))

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        name = form.name.data
        comment = form.comment.data

        feedback = Feedback(name=name, comment=comment)

        try:
            db.session.add(feedback)
            db.session.commit()
            flash('Feedback submitted successfully', 'success')
        except:
            flash('An error occurred while submitting feedback', 'error')

        return redirect(url_for('feedback'))

    feedback_data = Feedback.query.all()
    return render_template('feedback.html', form=form, feedback_data=feedback_data)

@app.route('/todo', methods=['GET', 'POST'])
def todo():
    form = TodoForm()

    if form.validate_on_submit():
        task = form.task.data
        new_todo = Todo(task=task)
        db.session.add(new_todo)
        db.session.commit()
        flash('Task added successfully!', 'success')
        return redirect(url_for('todo'))

    todos = Todo.query.all()
    return render_template('todo.html', form=form, todos=todos)

@app.route('/todo/update/<int:id>')
def update_todo(id):
    todo = Todo.query.get_or_404(id)
    todo.status = not todo.status  # Toggle status
    db.session.commit()
    flash('Task updated successfully!', 'success')
    return redirect(url_for('todo'))

@app.route('/todo/delete/<int:id>')
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('todo'))

@app.route('/users')
def users():
    return render_template('users.html', users=User.query.all())


# pic path #
UPLOAD_FOLDER = 'static/imgs/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
# end #

@app.before_request
def update_last_seen():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    update_account_form = UpdateAccountForm(obj=current_user)
    change_password_form = ChangePasswordForm()

    if update_account_form.validate_on_submit():
        current_user.username = update_account_form.username.data
        current_user.email = update_account_form.email.data

        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                current_user.image_file = filename

                # Move the file to the UPLOAD_FOLDER
                destination = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename)
                shutil.move(file_path, destination)

        db.session.commit()
        flash('Account updated successfully!', 'success')
        return redirect(url_for('account'))

    if change_password_form.validate_on_submit():
        if current_user.check_password(change_password_form.old_password.data):
            try:
                current_user.set_password(change_password_form.new_password.data)
                db.session.commit()
                flash('Password changed successfully!', 'success')
                return redirect(url_for('account'))
            except Exception as e:
                db.session.rollback()
                flash(f"Error changing password: {e}", 'danger')
        else:
            flash('Current password is incorrect', 'danger')


    return render_template('account.html', update_account_form=update_account_form, change_password_form=change_password_form, is_authenticated=True)






