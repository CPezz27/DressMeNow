import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from app import app


class AggiungiDatiSpedizioneTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_aggiungi_indirizzo_with_valid_input(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['logged_in'] = True
                sess['id'] = 1

            response = client.post('/indirizzo/aggiungi', data=dict(
                provincia='MI',
                cap='20121',
                via='Via Roma',
                tipo='Residenziale',
                citta='Milano'
            ), follow_redirects=True)

            self.assertIn(b"Indirizzo", response.data)

            if b"Indirizzo" in response.data:
                print("Test 'test_aggiungi_indirizzo_with_valid_input' PASSATO")
            else:
                print("Test 'test_aggiungi_indirizzo_with_valid_input' FALLITO")

    def test_aggiungi_indirizzo_with_invalid_user(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['logged_in'] = False

            response = client.post('/indirizzo/aggiungi', data=dict(
                provincia='MI',
                cap='20121',
                via='Via Roma',
                tipo='Residenziale',
                citta='Milano'
            ), follow_redirects=True)

            self.assertIn(b"Accedi", response.data)

            if b"Accedi" in response.data:
                print("Test 'test_aggiungi_indirizzo_with_invalid_user' PASSATO")
            else:
                print("Test 'test_aggiungi_indirizzo_with_invalid_user' FALLITO")


if __name__ == '__main__':
    unittest.main()
