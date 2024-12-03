# Author: Aditi Jha, December 2, 2024

# Unit Tests for testing movies tab features

import unittest
import sqlite3
import movies

# Creating a temporary database for testing
TEST_DATABASE = 'test_movie_reviews.db'

class TestMovies(unittest.TestCase):

    def setUp(self):
        """Setting up a test database and tables before each test."""
        self.conn = sqlite3.connect(TEST_DATABASE)
        self.cursor = self.conn.cursor()
        
        # Creating tables
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                genre TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                movie_id INTEGER NOT NULL,
                rating INTEGER NOT NULL,
                note TEXT NOT NULL,
                FOREIGN KEY (movie_id) REFERENCES movies (id)
            )
        ''')
        self.conn.commit()

        # Using test database for all operations
        movies.DATABASE = TEST_DATABASE

    def tearDown(self):
        """Cleaning up the database after each test."""
        self.cursor.execute('DROP TABLE IF EXISTS reviews')
        self.cursor.execute('DROP TABLE IF EXISTS movies')
        self.conn.commit()
        self.conn.close()

    def test_add_movie(self):
        """Testing adding a movie to the database."""
        response = movies.add_movie("Inception", "Science Fiction")
        self.cursor.execute('SELECT * FROM movies WHERE name = ?', ("Inception",))
        movie = self.cursor.fetchone()
        self.assertIsNotNone(movie)
        self.assertEqual(movie[1], "Inception")
        self.assertEqual(movie[2], "Science Fiction")
        self.assertEqual(response["message"], "Movie 'Inception' added successfully.")

    def test_add_review(self):
        """Testing adding a review to a movie."""
        movies.add_movie("Inception", "Science Fiction")
        response = movies.add_review(1, 5, "Amazing movie!")
        self.cursor.execute('SELECT * FROM reviews WHERE movie_id = ?', (1,))
        review = self.cursor.fetchone()
        self.assertIsNotNone(review)
        self.assertEqual(review[1], 1)
        self.assertEqual(review[2], 5)
        self.assertEqual(review[3], "Amazing movie!")
        self.assertEqual(response["message"], "Review added to movie ID 1.")

    def test_edit_review(self):
        """Testing editing a review."""
        movies.add_movie("Inception", "Science Fiction")
        movies.add_review(1, 4, "Good movie")
        response = movies.edit_review(1, 1, rating=5, note="Amazing movie!")
        self.cursor.execute('SELECT * FROM reviews WHERE id = 1')
        review = self.cursor.fetchone()
        self.assertEqual(review[2], 5)
        self.assertEqual(review[3], "Amazing movie!")
        self.assertEqual(response["message"], "Review ID 1 for movie ID 1 updated.")

    def test_delete_review(self):
        """Testing deleting a review."""
        movies.add_movie("Inception", "Science Fiction")
        movies.add_review(1, 5, "Amazing movie!")
        response = movies.delete_review(1, 1)
        self.cursor.execute('SELECT * FROM reviews WHERE id = 1')
        review = self.cursor.fetchone()
        self.assertIsNone(review)
        self.assertEqual(response["message"], "Review ID 1 deleted from movie ID 1.")

    def test_delete_movie(self):
        """Testing deleting a movie and its reviews."""
        movies.add_movie("Inception", "Science Fiction")
        movies.add_review(1, 5, "Amazing movie!")
        response = movies.delete_movie(1)
        self.cursor.execute('SELECT * FROM movies WHERE id = 1')
        movie = self.cursor.fetchone()
        self.cursor.execute('SELECT * FROM reviews WHERE movie_id = 1')
        review = self.cursor.fetchone()
        self.assertIsNone(movie)
        self.assertIsNone(review)
        self.assertEqual(response["message"], "Movie ID 1 and its reviews have been deleted.")

    def test_view_reviews(self):
        """Testing viewing all movies and their reviews."""
        movies.add_movie("Inception", "Science Fiction")
        movies.add_review(1, 5, "Amazing movie!")
        response = movies.view_reviews()
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]["name"], "Inception")
        self.assertEqual(response[0]["genre"], "Science Fiction")
        self.assertEqual(len(response[0]["reviews"]), 1)
        self.assertEqual(response[0]["reviews"][0]["note"], "Amazing movie!")

    def test_search_reviews(self):
        """Testing searching for reviews by movie ID."""
        movies.add_movie("Inception", "Science Fiction")
        movies.add_review(1, 5, "Amazing movie!")
        response = movies.search_reviews(1)
        self.assertEqual(response["name"], "Inception")
        self.assertEqual(response["genre"], "Science Fiction")
        self.assertEqual(len(response["reviews"]), 1)
        self.assertEqual(response["reviews"][0]["rating"], 5)

    def test_search_by_genre(self):
        """Testing searching for movies by genre."""
        movies.add_movie("Inception", "Science Fiction")
        movies.add_movie("Interstellar", "Science Fiction")
        response = movies.search_by_genre("Science Fiction")
        self.assertEqual(len(response), 2)
        self.assertEqual(response[0]["name"], "Inception")
        self.assertEqual(response[1]["name"], "Interstellar")

if __name__ == '__main__':
    unittest.main()
