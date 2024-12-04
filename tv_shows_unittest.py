# Author: Mastewal


import unittest
import sqlite3
import tv_shows  

# Creating a temporary database for testing
TEST_DATABASE = 'test_tvshows_rvw.db'

class TestTVShows(unittest.TestCase):

    def setUp(self):
        """Setting up a test database and table before each test."""
        self.conn = sqlite3.connect(TEST_DATABASE)
        self.cursor = self.conn.cursor()
        
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tv_shows (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                genre TEXT NOT NULL,
                rating REAL
            )
        ''')
        self.conn.commit()

        
        tv_shows.DATABASE = TEST_DATABASE

    def tearDown(self):
        """Cleaning up the database after each test."""
        self.cursor.execute('DROP TABLE IF EXISTS tv_shows')
        self.conn.commit()
        self.conn.close()

    def test_add_show_from_api(self):
        """Testing adding a TV show to the database."""
        response = tv_shows.add_show_from_api("Breaking Bad", "Drama", 9.5)
        self.cursor.execute('SELECT * FROM tv_shows WHERE title = ?', ("Breaking Bad",))
        show = self.cursor.fetchone()
        self.assertIsNotNone(show)
        self.assertEqual(show[1], "Breaking Bad")
        self.assertEqual(show[2], "Drama")
        self.assertEqual(show[3], 9.5)
        self.assertEqual(response["title"], "Breaking Bad")

    def test_get_show(self):
        """Testing getting a TV show by ID."""
        tv_shows.add_show_from_api("Breaking Bad", "Drama", 9.5)
        response = tv_shows.get_show(1)
        self.assertIsNotNone(response)
        self.assertEqual(response["title"], "Breaking Bad")
        self.assertEqual(response["genre"], "Drama")
        self.assertEqual(response["rating"], 9.5)

    def test_edit_show(self):
        """Testing editing a TV show."""
        tv_shows.add_show_from_api("Breaking Bad", "Drama", 9.5)
        response = tv_shows.edit_show(1, {"title": "Better Call Saul", "rating": 9.0})
        self.assertEqual(response["title"], "Better Call Saul")
        self.assertEqual(response["rating"], 9.0)

    def test_delete_show(self):
        """Testing deleting a TV show."""
        tv_shows.add_show_from_api("Breaking Bad", "Drama", 9.5)
        response = tv_shows.delete_show(1)
        self.assertTrue(response)
        self.cursor.execute('SELECT * FROM tv_shows WHERE id = 1')
        show = self.cursor.fetchone()
        self.assertIsNone(show)

    def test_filter_shows_by_genre(self):
        """Testing filtering TV shows by genre."""
        tv_shows.add_show_from_api("Breaking Bad", "Drama", 9.5)
        tv_shows.add_show_from_api("The Office", "Comedy", 8.9)
        response = tv_shows.filter_shows_by_genre("Drama")
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]["title"], "Breaking Bad")

   
if __name__ == '__main__':
    unittest.main()