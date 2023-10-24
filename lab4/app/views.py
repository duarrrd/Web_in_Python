from flask import render_template, request, abort, session, redirect, url_for, flash
from app import app
from datetime import datetime
import os
import json

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
    return render_template('main.html')

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
            return render_template('skill.html')
    else:
        return render_template('skills.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        with open(data_json_path, 'r') as json_file:
            auth_data = json.load(json_file)

        if username == auth_data['username'] and password == auth_data['password']:
            user_session['username'] = username

            return redirect(url_for('info'))

        error_message = "Authentication failed. Please check your username and password."

    return render_template('login.html', error_message=error_message)

@app.route('/info')
def info():
    if 'username' in user_session:
        username = user_session['username']
        return render_template('info.html', username=username)
    else:
        return redirect(url_for('login'))
