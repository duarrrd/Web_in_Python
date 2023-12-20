from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow

# Extensions
db = SQLAlchemy()
migrate = Migrate()
jwt_manager = JWTManager()
login_manager = LoginManager()
ma = Marshmallow()
