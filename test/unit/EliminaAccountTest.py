import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from app import app


class EliminaAccountTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_delete_account_with_valid_input(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['logged_in'] = True
                sess['id'] = 7

            response = client.post('/p/cancella_account', follow_redirects=True)

            self.assertIn(b'Crea un nuovo account!', response.data)

            if b"Crea un nuovo account!" in response.data:
                print("Test 'test_delete_account_with_valid_input' PASSATO")
            else:
                print("Test 'test_delete_account_with_valid_input' FALLITO")

    def test_delete_account_when_not_logged_in(self):
        with self.app as client:

            response = client.post('/p/cancella_account', follow_redirects=True)

            self.assertIn(b'Inserisci le tue credenziali!', response.data)

            if b"Inserisci le tue credenziali!" in response.data:
                print("Test 'test_delete_account_when_not_logged_in' PASSATO")
            else:
                print("Test 'test_delete_account_when_not_logged_in' FALLITO")


if __name__ == '__main__':
    unittest.main()
