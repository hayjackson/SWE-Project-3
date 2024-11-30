# Author: Aditi Jha, December 2, 2024

# Unit Tests for testing movies tab features

import unittest
from unittest.mock import patch, MagicMock
from movies import add_movie, add_review, edit_review, delete_review, delete_movie, view_movies, search_movies_by_genre, search_movie_by_id


class TestMovies(unittest.TestCase):
    @patch("movies.get_connection")
    def test_add_movie(self, mock_get_connection):
        # Mocking database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value
        mock_get_connection.return_value = mock_conn

        # Mocking cursor behavior for lastrowid
        mock_cursor.lastrowid = 1

        # Calling the function
        result = add_movie("Inception", "Sci-Fi")

        # Assertions
        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO movies (name, genre) VALUES (%s, %s)", ("Inception", "Sci-Fi")
        )
        mock_conn.commit.assert_called_once()
        self.assertEqual(result, {
            "message": "Movie 'Inception' added successfully.",
            "movie": {"id": 1, "name": "Inception", "genre": "Sci-Fi"}
        })

    @patch("movies.get_connection")
    def test_add_review(self, mock_get_connection):
        # Mocking database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value
        mock_get_connection.return_value = mock_conn

        # Mocking cursor behavior for lastrowid
        mock_cursor.lastrowid = 5

        # Calling the function
        result = add_review(1, 4.5, "Great movie!")

        # Assertions
        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO reviews (movie_id, rating, note) VALUES (%s, %s, %s)", (1, 4.5, "Great movie!")
        )
        mock_conn.commit.assert_called_once()
        self.assertEqual(result, {
            "message": "Review added to movie ID 1.",
            "review": {"review_id": 5, "rating": 4.5, "note": "Great movie!"}
        })

    @patch("movies.get_connection")
    def test_edit_review(self, mock_get_connection):
        # Mocking database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value
        mock_get_connection.return_value = mock_conn

        # Calling the function
        result = edit_review(1, 5, rating=4.0, note="Updated review")

        # Assertions
        mock_cursor.execute.assert_called_once_with(
            "UPDATE reviews SET rating = %s, note = %s WHERE movie_id = %s AND id = %s",
            (4.0, "Updated review", 1, 5)
        )
        mock_conn.commit.assert_called_once()
        self.assertEqual(result, {"message": "Review ID 5 for movie ID 1 updated."})

    @patch("movies.get_connection")
    def test_delete_review(self, mock_get_connection):
        # Mocking database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value
        mock_get_connection.return_value = mock_conn

        # Calling the function
        result = delete_review(1, 5)

        # Assertions
        mock_cursor.execute.assert_called_once_with(
            "DELETE FROM reviews WHERE movie_id = %s AND id = %s", (1, 5)
        )
        mock_conn.commit.assert_called_once()
        self.assertEqual(result, {"message": "Review ID 5 deleted from movie ID 1."})

    @patch("movies.get_connection")
    def test_delete_movie(self, mock_get_connection):
        # Mocking database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value
        mock_get_connection.return_value = mock_conn

        # Calling the function
        result = delete_movie(1)

        # Assertions
        mock_cursor.execute.assert_called_once_with(
            "DELETE FROM movies WHERE id = %s", (1,)
        )
        mock_conn.commit.assert_called_once()
        self.assertEqual(result, {"message": "Movie ID 1 and its reviews have been deleted."})

    @patch("movies.get_connection")
    def test_view_movies(self, mock_get_connection):
        # Mocking database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value
        mock_get_connection.return_value = mock_conn

        # Mocking database response
        mock_cursor.fetchall.return_value = [
            {"id": 1, "name": "Inception", "genre": "Sci-Fi"},
            {"id": 2, "name": "The Matrix", "genre": "Action"}
        ]

        # Calling the function
        result = view_movies()

        # Assertions
        mock_cursor.execute.assert_called_once_with("SELECT * FROM movies")
        self.assertEqual(result, [
            {"id": 1, "name": "Inception", "genre": "Sci-Fi"},
            {"id": 2, "name": "The Matrix", "genre": "Action"}
        ])

        
    @patch("movies.get_connection")
    def test_search_movies_by_genre(self, mock_get_connection):
        # Mocking database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value
        mock_get_connection.return_value = mock_conn

        # Mocking database response
        mock_cursor.fetchall.return_value = [
            {"id": 1, "name": "Inception", "genre": "Sci-Fi"}
        ]

        # Calling the function
        result = search_movies_by_genre("Sci-Fi")

        # Assertions
        mock_cursor.execute.assert_called_once_with("SELECT * FROM movies WHERE genre = %s", ("Sci-Fi",))
        self.assertEqual(result, [{"id": 1, "name": "Inception", "genre": "Sci-Fi"}])

    @patch("movies.get_connection")
    def test_search_movie_by_id(self, mock_get_connection):
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value
        mock_get_connection.return_value = mock_conn

        # Mocking a valid movie response
        mock_cursor.fetchone.return_value = {"id": 1, "name": "Inception", "genre": "Sci-Fi"}

        # Valid ID test
        result = search_movie_by_id(1)
        mock_cursor.execute.assert_called_once_with("SELECT * FROM movies WHERE id = %s", (1,))
        self.assertEqual(result, {"message": "Movie found.", "movie": {"id": 1, "name": "Inception", "genre": "Sci-Fi"}})

        # Resetting mocks for invalid ID test
        mock_cursor.reset_mock()
        mock_cursor.fetchone.return_value = None

        # Invalid ID test
        result = search_movie_by_id(99)
        mock_cursor.execute.assert_called_once_with("SELECT * FROM movies WHERE id = %s", (99,))
        self.assertEqual(result, {"error": "Movie with ID 99 not found."})
    
    


if __name__ == "__main__":
    unittest.main()
