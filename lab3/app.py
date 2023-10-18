from flask import Flask, render_template, request
from datetime import datetime
import os

app = Flask(__name__)


@app.route('/')
def main():
    OS = os.environ['OS']
    u_agent = request.user_agent
    time = datetime.now().strftime("%H:%M")
    return render_template('main.html', u_agent=u_agent, time=time, OS=OS)

@app.route('/l_and_s')
def l_and_s():
    return render_template('L&S.html')

@app.route('/skills')
def skills():
    return render_template('skills.html')


if __name__ == '__main__':
    app.run()
