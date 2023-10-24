from flask import render_template, request, abort
from app import app
from datetime import datetime
import os

my_skills = [
    "Python",
    "HTML",
    "CSS",
    "JS",
]

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

@app.route('/login')
def login():
    return render_template('login.html')