# Author: Aditi Jha, December 2, 2024

# Integration tests for movies tab:

import unittest
import json
from api import app
import movies

class TestMoviesIntegration(unittest.TestCase):
    def setUp(self):
        """Setting up the test client and configuring the test database."""
        self.app = app.test_client()
        self.app.testing = True

        # Using a test database for integration testing
        movies.DATABASE = 'test_movie_reviews.db'
        with movies.sqlite3.connect(movies.DATABASE) as conn:
            cursor = conn.cursor()
            # Create the movies table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS movies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    genre TEXT NOT NULL
                )
            ''')
            # Creating the reviews table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    movie_id INTEGER NOT NULL,
                    rating INTEGER NOT NULL,
                    note TEXT NOT NULL,
                    FOREIGN KEY (movie_id) REFERENCES movies (id)
                )
            ''')
            conn.commit()

    def tearDown(self):
        """Cleaning up the test database after each test."""
        with movies.sqlite3.connect(movies.DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('DROP TABLE IF EXISTS reviews')
            cursor.execute('DROP TABLE IF EXISTS movies')
            conn.commit()

    def test_add_movie(self):
        """Testing the POST /movies endpoint."""
        response = self.app.post(
            '/movies',
            data=json.dumps({"name": "Inception", "genre": "Science Fiction"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("Movie 'Inception' added successfully.", response.get_data(as_text=True))

    def test_add_review(self):
        """Testing the POST /movies/<int:movie_id>/reviews endpoint."""
        # First, adding a movie
        self.app.post(
            '/movies',
            data=json.dumps({"name": "Inception", "genre": "Science Fiction"}),
            content_type='application/json'
        )
        # Then, adding a review
        response = self.app.post(
            '/movies/1/reviews',
            data=json.dumps({"rating": 5, "note": "Amazing movie!"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("Review added to movie ID 1.", response.get_data(as_text=True))

    def test_edit_review(self):
        """Testing the PUT /movies/<int:movie_id>/reviews/<int:review_id> endpoint."""
        # Adding a movie and a review
        self.app.post(
            '/movies',
            data=json.dumps({"name": "Inception", "genre": "Science Fiction"}),
            content_type='application/json'
        )
        self.app.post(
            '/movies/1/reviews',
            data=json.dumps({"rating": 4, "note": "Good movie"}),
            content_type='application/json'
        )
        # Editing the review
        response = self.app.put(
            '/movies/1/reviews/1',
            data=json.dumps({"rating": 5, "note": "Amazing movie!"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Review ID 1 for movie ID 1 updated.", response.get_data(as_text=True))

    def test_delete_review(self):
        """Testing the DELETE /movies/<int:movie_id>/reviews/<int:review_id> endpoint."""
        # Adding a movie and a review
        self.app.post(
            '/movies',
            data=json.dumps({"name": "Inception", "genre": "Science Fiction"}),
            content_type='application/json'
        )
        self.app.post(
            '/movies/1/reviews',
            data=json.dumps({"rating": 5, "note": "Amazing movie!"}),
            content_type='application/json'
        )
        # Deleting the review
        response = self.app.delete('/movies/1/reviews/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Review ID 1 deleted from movie ID 1.", response.get_data(as_text=True))

    def test_delete_movie(self):
        """Testing the DELETE /movies/<int:movie_id> endpoint."""
        # Adding a movie
        self.app.post(
            '/movies',
            data=json.dumps({"name": "Inception", "genre": "Science Fiction"}),
            content_type='application/json'
        )
        # Deleting the movie
        response = self.app.delete('/movies/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Movie ID 1 and its reviews have been deleted.", response.get_data(as_text=True))

    def test_view_reviews(self):
        """Testing the GET /movies endpoint."""
        # Adding a movie and a review
        self.app.post(
            '/movies',
            data=json.dumps({"name": "Inception", "genre": "Science Fiction"}),
            content_type='application/json'
        )
        self.app.post(
            '/movies/1/reviews',
            data=json.dumps({"rating": 5, "note": "Amazing movie!"}),
            content_type='application/json'
        )
        # Viewing reviews
        response = self.app.get('/movies')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], "Inception")
        self.assertEqual(data[0]['genre'], "Science Fiction")

    def test_search_reviews(self):
        """Testing the GET /movies/<int:movie_id>/reviews endpoint."""
        # Adding a movie and a review
        self.app.post(
            '/movies',
            data=json.dumps({"name": "Inception", "genre": "Science Fiction"}),
            content_type='application/json'
        )
        self.app.post(
            '/movies/1/reviews',
            data=json.dumps({"rating": 5, "note": "Amazing movie!"}),
            content_type='application/json'
        )
        # Searching reviews
        response = self.app.get('/movies/1/reviews')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['name'], "Inception")
        self.assertEqual(data['genre'], "Science Fiction")
        self.assertEqual(len(data['reviews']), 1)
        self.assertEqual(data['reviews'][0]['note'], "Amazing movie!")

    def test_search_by_genre(self):
        """Testing the GET /movies/genre endpoint."""
        # Adding movies
        self.app.post(
            '/movies',
            data=json.dumps({"name": "Inception", "genre": "Science Fiction"}),
            content_type='application/json'
        )
        self.app.post(
            '/movies',
            data=json.dumps({"name": "Interstellar", "genre": "Science Fiction"}),
            content_type='application/json'
        )
        # Searching by genre
        response = self.app.get('/movies/genre?genre=Science Fiction')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], "Inception")
        self.assertEqual(data[1]['name'], "Interstellar")

if __name__ == '__main__':
    unittest.main()
