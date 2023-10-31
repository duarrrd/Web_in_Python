from flask import render_template, request, session, redirect, url_for, flash, make_response
from app import app
from datetime import datetime
import os
import json
from app.form import LoginForm

my_skills = [
    "Python",
    "HTML",
    "CSS",
    "JS",
]

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
    error_message = None

    form = LoginForm()

    if form.validate_on_submit():
        username = form.name.data
        password = form.password.data
        remember = form.remember.data

        with open(data_json_path, 'r') as json_file:
            auth_data = json.load(json_file)

        if username == auth_data['username'] and password == auth_data['password']:
            user_session['username'] = username

            if remember:
                session.permanent = True

            flash("Login successful.", "success")

            return redirect(url_for('info'))

        error_message = "Authentication failed. Please check your username and password."

    return render_template('login.html', error_message=error_message, form=form)

@app.route('/info', methods=['GET', 'POST'])
def info():
    if 'username' in user_session:
        username = user_session['username']

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

        return render_template('info.html', username=username, cookies=cookies)
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


@app.route('/logout', methods=['POST'])
def logout():
    if 'username' in user_session:
        del user_session['username']

    return redirect(url_for('login'))

@app.route('/change_password', methods=['POST'])
def change_password():
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')

    username = user_session['username']

    with open(data_json_path, 'r') as json_file:
        auth_data = json.load(json_file)

    if username == auth_data['username'] and old_password == auth_data['password']:
        auth_data['password'] = new_password

        with open(data_json_path, 'w') as json_file:
            json.dump(auth_data, json_file)

        flash('Password changed successfully.', 'success')

        return redirect(url_for('info'))
    else:
        flash('Invalid password.', 'error')

        return redirect(url_for('info'))
