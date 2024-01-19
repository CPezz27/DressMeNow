import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from app import app
from flask import session


class SearchProductsTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_search_products_with_valid_input(self):
        response = self.app.get('/search', query_string=dict(product_name='capra'), follow_redirects=True)

        self.assertNotIn(b'Non abbiamo trovato nessun prodotto con questo nome', response.data)

    def test_search_products_with_incorrect_input(self):
        response = self.app.get('/search', query_string=dict(product_name='ewtewtewtewt'), follow_redirects=True)

        self.assertIn(b'Non abbiamo trovato nessun prodotto con questo nome', response.data)


if __name__ == '__main__':
    unittest.main()
