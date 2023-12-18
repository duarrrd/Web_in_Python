# tests/flask_testing/base_test.py
from flask_testing import TestCase
from app import create_app, db

class BaseTest(TestCase):
    def create_app(self):
        app = create_app(config_name='TEST')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
