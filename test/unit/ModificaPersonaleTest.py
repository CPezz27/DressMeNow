import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from app import app
from flask import session
from urllib.parse import urlparse, parse_qs


class ModificaPersonaleTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_modifica_personale_with_valid_input(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['logged_in'] = True
                sess['ruolo'] = 'direttore'

            personal_id = 5

            response = client.post(f'/d/modifica_personale/{personal_id}', data=dict(
                tipo_personale='gestore_ordine'
            ), follow_redirects=True)

            self.assertIn(b'Personale modificato', response.data)

    def test_modifica_personale_with_invalid_role(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['logged_in'] = True
                sess['ruolo'] = 'gestore_ordine'

            personal_id = 1

            response = client.post(f'/d/modifica_personale/{personal_id}', data=dict(), follow_redirects=True)

            self.assertIn(b'Inserisci le tue credenziali!', response.data)


if __name__ == '__main__':
    unittest.main()
