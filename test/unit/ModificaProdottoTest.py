import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from app import app


class ModificaProdottoTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_modifica_prodotto_with_valid_input(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['logged_in'] = True
                sess['ruolo'] = 'gestore_prodotto'

            product_id = 1  # Replace with a valid product ID in your test database

            response = client.post(f'/gp/modifica_prodotto/{product_id}', data=dict(
                descrizione='Nuova descrizione del prodotto'
            ), follow_redirects=True)

            self.assertIn(b'Prodotto modificato correttamente', response.data)

    def test_modifica_prodotto_with_invalid_role(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['logged_in'] = True
                sess['ruolo'] = 'utente'

            product_id = 1

            response = client.post(f'/gp/modifica_prodotto/{product_id}', data=dict(), follow_redirects=True)

            self.assertIn(b'Uomo', response.data)


if __name__ == '__main__':
    unittest.main()
