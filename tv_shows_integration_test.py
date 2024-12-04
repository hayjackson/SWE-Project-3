# Author: Mastewal, December 3, 2024



import unittest
import json
from api import app
import tv_shows

class TestTVShowsIntegration(unittest.TestCase):
    def setUp(self):
        """Setting up the test client and configuring the test database."""
        self.app = app.test_client()
        self.app.testing = True

        # Using a test database for integration testing
        tv_shows.DATABASE = 'test_tvshows_rvw.db'
        with tv_shows.sqlite3.connect(tv_shows.DATABASE) as conn:
            cursor = conn.cursor()
            # Create the tv_shows table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tv_shows (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    genre TEXT NOT NULL,
                    rating REAL
                )
            ''')
            conn.commit()

    def tearDown(self):
        """Cleaning up the test database after each test."""
        with tv_shows.sqlite3.connect(tv_shows.DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('DROP TABLE IF EXISTS tv_shows')
            conn.commit()

    def test_add_show(self):
        """Testing the POST /tv_shows endpoint."""
        response = self.app.post(
            '/tv_shows',
            data=json.dumps({"title": "Breaking Bad", "genre": "Drama", "rating": 9.5}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("TV show 'Breaking Bad' added successfully.", response.get_data(as_text=True))

    def test_get_show(self):
        """Testing the GET /tv_shows/<int:show_id> endpoint."""
        # First, add a show
        self.app.post(
            '/tv_shows',
            data=json.dumps({"title": "Breaking Bad", "genre": "Drama", "rating": 9.5}),
            content_type='application/json'
        )
        # get the show
        response = self.app.get('/tv_shows/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['title'], "Breaking Bad")
        self.assertEqual(data['genre'], "Drama")
        self.assertEqual(data['rating'], 9.5)

    def test_edit_show(self):
        """Testing the PUT /tv_shows/<int:show_id> endpoint."""
        # Add a show
        self.app.post(
            '/tv_shows',
            data=json.dumps({"title": "Breaking Bad", "genre": "Drama", "rating": 9.5}),
            content_type='application/json'
        )
        # Edit the show
        response = self.app.put(
            '/tv_shows/1',
            data=json.dumps({"title": "Better Call Saul", "rating": 9.0}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['title'], "Better Call Saul")
        self.assertEqual(data['rating'], 9.0)

    def test_delete_show(self):
        """Testing the DELETE /tv_shows/<int:show_id> endpoint."""
        # Add a show
        self.app.post(
            '/tv_shows',
            data=json.dumps({"title": "Breaking Bad", "genre": "Drama", "rating": 9.5}),
            content_type='application/json'
        )
        # Delete the show
        response = self.app.delete('/tv_shows/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn("TV show ID 1 has been deleted.", response.get_data(as_text=True))

    def test_filter_shows_by_genre(self):
        """Testing the GET /tv_shows/genre endpoint."""
        # Add shows
        self.app.post(
            '/tv_shows',
            data=json.dumps({"title": "Breaking Bad", "genre": "Drama", "rating": 9.5}),
            content_type='application/json'
        )
        self.app.post(
            '/tv_shows',
            data=json.dumps({"title": "The Office", "genre": "Comedy", "rating": 8.9}),
            content_type='application/json'
        )
        # Filter by genre
        response = self.app.get('/tv_shows/genre?genre=Drama')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], "Breaking Bad")

if __name__ == '__main__':
    unittest.main()