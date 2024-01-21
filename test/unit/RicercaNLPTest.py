import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from app import app
import unittest


class RicercaNLPTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_search_with_valid_query(self):
        response = self.app.post('/ricercaNLP', data=dict(
            text='voglio una maglia'
        ), follow_redirects=True)

        self.assertIn(b'Vestibilit', response.data)

        if b'Vestibilit' in response.data:
            print("Test 'test_search_with_valid_query' PASSATO")
        else:
            print("Test 'test_search_with_valid_query' FALLITO")

    def test_search_with_empty_query(self):
        response = self.app.post('/ricercaNLP', data=dict(
            text=''
        ), follow_redirects=True)

        self.assertIn(b'non abbiamo trovato prodotti', response.data)

        if b'non abbiamo trovato prodotti' in response.data:
            print("Test 'test_search_with_empty_query' PASSATO")
        else:
            print("Test 'test_search_with_empty_query' FALLITO")


if __name__ == '__main__':
    unittest.main()
