import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from app import app


class RegisterTest(unittest.TestCase):

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
            email='john.doe@example57.com',
            confirmPassword='Password1234!'
        ), follow_redirects=True)

        self.assertIn(b'Accedi', response.data)

        if b"Accedi" in response.data:
            print("Test 'test_registration_with_valid_data' PASSATO")
        else:
            print("Test 'test_registration_with_valid_data' FALLITO")

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

        if b"Dati inseriti non validi. Controlla i campi e riprova." in response.data:
            print("Test 'test_registration_with_invalid_data' PASSATO")
        else:
            print("Test 'test_registration_with_invalid_data' FALLITO")


if __name__ == '__main__':
    unittest.main()
