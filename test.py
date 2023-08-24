from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.secret_key = 'Boggle_KEY'


class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))


    def test_valid_word(self):
        """Test if word is valid by modifying the board in the session"""

        with self.client.session_transaction() as sess:
            sess['board'] = [["A", "L", "P", "H", "A"],
                             ["A", "L", "P", "H", "A"],
                             ["A", "L", "P", "H", "A"],
                             ["A", "L", "P", "H", "A"],
                             ["A", "L", "P", "H", "A"]]
        response = self.client.post('/validate-guess', json={'word': 'alpha'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        """Test if word is in the dictionary"""

        with self.client.session_transaction() as sess:
            sess['board'] = [["A", "L", "P", "H", "A"],
                             ["A", "L", "P", "H", "A"],
                             ["A", "L", "P", "H", "A"],
                             ["A", "L", "P", "H", "A"],
                             ["A", "L", "P", "H", "A"]]

        self.client.post('/')
        response = self.client.post('/validate-guess', json={'word': 'bravo'})
        # print(response.json)
        self.assertEqual(response.json["result"], 'not-on-board')

    def test_not_a_word(self):
        """Test if word is in the dictionary"""

        with self.client.session_transaction() as sess:
            sess['board'] = [["A", "L", "P", "H", "A"],
                             ["A", "L", "P", "H", "A"],
                             ["A", "L", "P", "H", "A"],
                             ["A", "L", "P", "H", "A"],
                             ["A", "L", "P", "H", "A"]]

        self.client.post('/')
        response = self.client.post('/validate-guess', json={'word': 'xray'})
        # print(response.json)
        self.assertEqual(response.json["result"], 'not-a-word')
