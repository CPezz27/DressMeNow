import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from app import app
import unittest


class LoginTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_login_with_valid_credentials(self):
        response = self.app.post('/login', data=dict(
            email='alrossi@gmail.com',
            password='Password1234!'
        ), follow_redirects=True)

        self.assertIn(b'Bentornato', response.data)

    def test_login_with_invalid_credentials(self):
        response = self.app.post('/login', data=dict(
            email='invalid@example.com',
            password='Password1234!'
        ), follow_redirects=True)

        self.assertIn(b'Credenziali non valide. Riprova.', response.data)

    def test_login_with_invalid_parameters(self):
        response = self.app.post('/login', data=dict(
            email='invalid@example.com',
            password='wrong_password'
        ), follow_redirects=True)

        self.assertIn(b'La password non rispetta i criteri richiesti.', response.data)


if __name__ == '__main__':
    unittest.main()
