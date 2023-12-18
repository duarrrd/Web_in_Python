# tests/flask_testing/test_views.py
from flask import url_for
from .base_test import BaseTest
from app.profile.models import User


class ViewsTest(BaseTest):

    # >>>>>>>>>>>>>
    # Resume test starts
    # >>>>>>>>>>>>>

    def test_main_page(self):
        response = self.client.get(url_for('resume.main'))
        self.assert200(response)
        self.assertIn(b'EDUARD BRYLIUK', response.data)

    def test_skills_page(self):
        response = self.client.get(url_for('resume.skills'))
        self.assert200(response)
        self.assertIn(b'List of Skills', response.data)

    def test_licenses_and_certifications_page(self):
        response = self.client.get(url_for('resume.licenses_and_certifications'))
        self.assert200(response)
        self.assertIn(b'IBM Full Stack', response.data)

    # TEST-END
    # >>>>>>>>>>>>>
    # Profile test starts
    # >>>>>>>>>>>>>

    def test_login_page(self):
        response = self.client.get(url_for('profile.login'), follow_redirects=True)
        self.assert200(response)
        self.assertIn(b'Email', response.data)

    def test_registration_page(self):
        response = self.client.get(url_for('profile.registration'), follow_redirects=True)
        self.assert200(response)
        self.assertIn(b'Username', response.data)

    def test_user_registration(self):
        response = self.client.post(
            url_for('profile.registration'),
            data={'username': 'test_user', 'email': 'test@example.com', 'password': 'test_password', 'confirm_password': 'test_password'}
        , follow_redirects=True)
        self.assert200(response)
        self.assertIsInstance(User.query.filter_by(username='test_user').first(), User)

    def test_user_login_logout(self):
        response = self.client.post(
            url_for('profile.login'),
            data={'email': 'test@example.com', 'password': 'test_password'}
        , follow_redirects=True)
        self.assert200(response)

        response = self.client.get(url_for('profile.logout'), follow_redirects=True)
        self.assert200(response)

    def test_change_password(self):
        self.client.post('/login', data=dict(email='test@example.com', password='test_password'))

        response = self.client.post(
            url_for('profile.change_password'),
            data={'old_password': 'test_password', 'new_password': 'new_test_password'},
            follow_redirects=True
        )

        self.assert200(response)

    def test_users_page(self):
        response = self.client.get(url_for('profile.users'), follow_redirects=True)
        self.assert200(response)
        self.assertIn(b'Number of users', response.data)
