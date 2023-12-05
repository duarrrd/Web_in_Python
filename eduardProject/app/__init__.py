from flask import Flask
from config import config
from .extensions import db, migrate, login_manager

def create_app(config_name='DEF'):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name))

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Configure login_manager
    login_manager.login_view = 'profile.login'
    login_manager.login_message_category = 'cookies.info'

    with app.app_context():
        # Import and register blueprints
        from app.resume.views import resume_bp
        from app.cookies.views import cookies_bp
        from app.profile.views import profile_bp
        from app.todo.views import todo_bp
        from app.feedback.views import feedback_bp

        app.register_blueprint(resume_bp, url_prefix='/')
        app.register_blueprint(cookies_bp, url_prefix='/cookies')
        app.register_blueprint(profile_bp, url_prefix='/profile')
        app.register_blueprint(todo_bp, url_prefix='/todo')
        app.register_blueprint(feedback_bp, url_prefix='/feedback')

    return app
