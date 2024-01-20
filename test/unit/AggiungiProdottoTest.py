import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from app import app


class AggiungiProdottoTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_aggiungi_prodotto_with_valid_input(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['logged_in'] = True
                sess['ruolo'] = 'gestore_prodotto'

            response = client.post('/gp/aggiungi_prodotto', data=dict(
                nome='Prodotto Test',
                categoria='Categoria Test',
                marca='Marca Test',
                descrizione='Descrizione Test',
                vestibilita='Vestibilità Test',
                prezzo='50.00',
                colore='Colore Test',
                materiale='Materiale Test'
            ), follow_redirects=True)

            self.assertIn(b"taglie", response.data)

            if b"taglie" in response.data:
                print("Test 'test_aggiungi_prodotto_with_valid_input' PASSATO")
            else:
                print("Test 'test_aggiungi_prodotto_with_valid_input' FALLITO")

    def test_aggiungi_prodotto_with_invalid_role(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['logged_in'] = True
                sess['ruolo'] = 'gestore_ordine'

            response = client.post('/gp/aggiungi_prodotto', data=dict(
                nome='Prodotto Test',
                categoria='Categoria Test',
                marca='Marca Test',
                descrizione='Descrizione Test',
                vestibilita='Vestibilità Test',
                prezzo='50.00',
                colore='Colore Test',
                materiale='Materiale Test'
            ), follow_redirects=True)

            self.assertIn(b"Uomo", response.data)

            if b"Uomo" in response.data:
                print("Test 'test_aggiungi_prodotto_with_invalid_role' PASSATO")
            else:
                print("Test 'test_aggiungi_prodotto_with_invalid_role' FALLITO")


if __name__ == '__main__':
    unittest.main()
