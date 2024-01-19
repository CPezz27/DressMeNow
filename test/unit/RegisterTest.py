import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from app import app


class RegistrationTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_registration_with_valid_data(self):
        response = self.app.post('/registrati', data=dict(
            firstName='John',
            lastName='Doe',
            dataNascita='1990-01-01',
            NumeroTelefonico='1234567890',
            sesso='uomo',
            email='john.doe@example55.com',
            confirmPassword='Password1234!'
        ), follow_redirects=True)

        self.assertIn(b'Accedi', response.data)

    def test_registration_with_invalid_data(self):
        response = self.app.post('/registrati', data=dict(
            firstName='John',
            lastName='Doe',
            dataNascita='1990-01-01',
            NumeroTelefonico='1234567890',
            sesso='invalid_gender',
            email='invalid_email',
            confirmPassword='invalid_password'
        ), follow_redirects=True)

        self.assertIn(b'Dati inseriti non validi. Controlla i campi e riprova.', response.data)


if __name__ == '__main__':
    unittest.main()
