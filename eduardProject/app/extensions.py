from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_jwt_extended import JWTManager

# Extensions
db = SQLAlchemy()
migrate = Migrate()
jwt_manager = JWTManager()
login_manager = LoginManager()
