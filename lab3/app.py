from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def main():  # put application's code here
    return render_template('main.html')

@app.route('/l_and_s')
def l_and_s():  # put application's code here
    return render_template('L&S.html')

@app.route('/skills')
def skills():  # put application's code here
    return render_template('skills.html')


if __name__ == '__main__':
    app.run()
