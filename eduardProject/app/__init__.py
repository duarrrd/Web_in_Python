from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'  # Change the database URI as needed
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import views