import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from app import app


class ModificaOrdineTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_modifica_ordine_with_valid_input(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['logged_in'] = True
                sess['ruolo'] = 'gestore_ordine'

            order_id = 16

            response = client.post('/go/modifica_ordine', data=dict(
                id_ordine=order_id,
                nuovo_stato='Consegnato'
            ), follow_redirects=True)

            self.assertIn(b"Stato ordine modificato correttamente", response.data)

    def test_modifica_ordine_with_invalid_role(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['logged_in'] = True
                sess['ruolo'] = 'gestore_prodotto'

            order_id = 16

            response = client.post('/go/modifica_ordine', data=dict(
                id_ordine=order_id,
                nuovo_stato='Consegnato'
            ), follow_redirects=True)

            self.assertIn(b'Uomo', response.data)


if __name__ == '__main__':
    unittest.main()
