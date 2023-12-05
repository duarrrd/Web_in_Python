import os
from flask import render_template, redirect, request, abort
from datetime import datetime
from . import resume_bp

my_skills = ["Python", "HTML", "CSS", "JS"]

@resume_bp.route('/')
def main():
    OS = os.environ.get('OS', 'Unknown')
    u_agent = request.user_agent
    time = datetime.now().strftime("%H:%M")
    return render_template('main.html', u_agent=u_agent, time=time, OS=OS)

@resume_bp.route('/l_and_s')
def licenses_and_certifications():
    return render_template('L&S.html')

@resume_bp.route('/skills/<int:id>')
@resume_bp.route('/skills')
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
