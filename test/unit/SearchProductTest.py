import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from app import app


class SearchProductsTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_search_products_with_valid_input(self):
        response = self.app.get('/search', query_string=dict(product_name='capra'), follow_redirects=True)

        self.assertNotIn(b'Non abbiamo trovato nessun prodotto con questo nome', response.data)

        if b"Non abbiamo trovato nessun prodotto con questo nome" in response.data:
            print("Test 'test_search_products_with_valid_input' PASSATO")
        else:
            print("Test 'test_search_products_with_valid_input' FALLITO")

    def test_search_products_with_incorrect_input(self):
        response = self.app.get('/search', query_string=dict(product_name='ewtewtewtewt'), follow_redirects=True)

        self.assertIn(b'Non abbiamo trovato nessun prodotto con questo nome', response.data)

        if b"Non abbiamo trovato nessun prodotto con questo nome" in response.data:
            print("Test 'test_search_products_with_incorrect_input' PASSATO")
        else:
            print("Test 'test_search_products_with_incorrect_input' FALLITO")


if __name__ == '__main__':
    unittest.main()
