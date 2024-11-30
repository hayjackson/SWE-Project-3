# Author: Aditi Jha, December 2, 2024

# Integration tests for movies tab:

import unittest
import requests
import os
from movies_db import get_connection

class TestMoviesIntegration(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5000/movies"

    def setUp(self):
        """
        Reset the database before each test.
        """
        self.reset_database()

    def reset_database(self):
        """
        Clears the movies and reviews tables in the database.
        """
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM reviews")
        cursor.execute("DELETE FROM movies")
        connection.commit()
        connection.close()

    def test_add_movie(self):
        """
        Test adding a new movie with genre via the API.
        """
        payload = {"name": "Inception", "genre": "Sci-Fi"}
        response = requests.post(self.BASE_URL, json=payload)
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertEqual(response_data["movie"]["name"], "Inception")
        self.assertEqual(response_data["movie"]["genre"], "Sci-Fi")

    def test_view_movies(self):
        """
        Test viewing all movies via the API.
        """
        # Add a movie
        payload = {"name": "Interstellar", "genre": "Sci-Fi"}
        requests.post(self.BASE_URL, json=payload)

        # Add another movie
        payload = {"name": "The Dark Knight", "genre": "Action"}
        requests.post(self.BASE_URL, json=payload)

        # View all movies
        response = requests.get(self.BASE_URL)
        self.assertEqual(response.status_code, 200)
        movies = response.json()
        self.assertEqual(len(movies), 2)
        self.assertEqual(movies[0]["name"], "Interstellar")
        self.assertEqual(movies[1]["name"], "The Dark Knight")

    def test_add_review(self):
        """
        Test adding a review to a movie via the API.
        """
        # Add a movie
        payload = {"name": "Inception", "genre": "Sci-Fi"}
        movie_response = requests.post(self.BASE_URL, json=payload)
        movie_id = movie_response.json()["movie"]["id"]

        # Add a review to the movie
        review_url = f"{self.BASE_URL}/{movie_id}/reviews"
        review_payload = {"rating": 5, "note": "Amazing movie!"}
        response = requests.post(review_url, json=review_payload)
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertEqual(response_data["review"]["rating"], 5)
        self.assertEqual(response_data["review"]["note"], "Amazing movie!")

    def test_delete_movie(self):
        """
        Test deleting a movie via the API.
        """
        # Add a movie
        payload = {"name": "Avatar", "genre": "Sci-Fi"}
        movie_response = requests.post(self.BASE_URL, json=payload)
        movie_id = movie_response.json()["movie"]["id"]

        # Delete the movie
        delete_url = f"{self.BASE_URL}/{movie_id}"
        response = requests.delete(delete_url)
        self.assertEqual(response.status_code, 200)

        # Check that the movie no longer exists
        response = requests.get(self.BASE_URL)
        movies = response.json()
        self.assertEqual(len(movies), 0)

    def test_search_movies_by_genre(self):
        """
        Test searching movies by genre via the API.
        """
        # Add movies
        requests.post(self.BASE_URL, json={"name": "Inception", "genre": "Sci-Fi"})
        requests.post(self.BASE_URL, json={"name": "The Dark Knight", "genre": "Action"})

        # Search for Sci-Fi movies
        genre_url = f"{self.BASE_URL}/genre/Sci-Fi"
        response = requests.get(genre_url)
        self.assertEqual(response.status_code, 200)
        movies = response.json()
        self.assertEqual(len(movies), 1)
        self.assertEqual(movies[0]["name"], "Inception")

    def test_edit_review(self):
        """
        Test editing a review via the API.
        """
        # Add a movie
        payload = {"name": "Inception", "genre": "Sci-Fi"}
        movie_response = requests.post(self.BASE_URL, json=payload)
        movie_id = movie_response.json()["movie"]["id"]

        # Add a review to the movie
        review_url = f"{self.BASE_URL}/{movie_id}/reviews"
        review_payload = {"rating": 4, "note": "Good movie!"}
        review_response = requests.post(review_url, json=review_payload)
        review_id = review_response.json()["review"]["review_id"]

        # Edit the review
        edit_url = f"{self.BASE_URL}/{movie_id}/reviews/{review_id}"
        edit_payload = {"rating": 5, "note": "Great movie!"}
        response = requests.put(edit_url, json=edit_payload)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["message"], f"Review ID {review_id} for movie ID {movie_id} updated.")

    def test_delete_review(self):
        """
        Test deleting a review via the API.
        """
        # Add a movie
        payload = {"name": "Inception", "genre": "Sci-Fi"}
        movie_response = requests.post(self.BASE_URL, json=payload)
        movie_id = movie_response.json()["movie"]["id"]

        # Add a review to the movie
        review_url = f"{self.BASE_URL}/{movie_id}/reviews"
        review_payload = {"rating": 4, "note": "Good movie!"}
        review_response = requests.post(review_url, json=review_payload)
        review_id = review_response.json()["review"]["review_id"]

        # Delete the review
        delete_url = f"{self.BASE_URL}/{movie_id}/reviews/{review_id}"
        response = requests.delete(delete_url)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
