from flask import Flask, render_template, request, abort
from datetime import datetime
import os

app = Flask(__name__)

my_skills = [
    "Python",
    "HTML",
    "CSS",
    "JS",
]

@app.route('/')
def main():
    OS = os.environ['OS']
    u_agent = request.user_agent
    time = datetime.now().strftime("%H:%M")
    return render_template('main.html', u_agent=u_agent, time=time, OS=OS)

@app.route('/l_and_s')
def l_and_s():
    OS = os.environ['OS']
    u_agent = request.user_agent
    time = datetime.now().strftime("%H:%M")
    return render_template('L&S.html', u_agent=u_agent, time=time, OS=OS)

@app.route('/skills/<int:id>')
@app.route('/skills')
def skills(id=None):
    OS = os.environ['OS']
    u_agent = request.user_agent
    time = datetime.now().strftime("%H:%M")

    if id is not None:
        if id > len(my_skills):
            abort(404)
        else:
            index = id - 1
            skill = my_skills[index]
            return render_template('skill.html', skill=skill, id=id, u_agent=u_agent, time=time, OS=OS)
    else:
        return render_template('skills.html', my_skills=my_skills, u_agent=u_agent, time=time, OS=OS)

if __name__ == '__main__':
    app.run()
