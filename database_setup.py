# Author: Aditi Jha, December 2, 2024
# Setting up sqlite3 database for the project

import sqlite3



# Movies tab database, author Aditi, december 2, 2024
def initialize_db():
    conn = sqlite3.connect('movie_reviews.db')
    cursor = conn.cursor()
    
    # Creating  movies table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            genre TEXT NOT NULL
        )
    ''')

    # Creating reviews table
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
    conn.close()
# Tv_shows
def initialize_tvshow_db():
    """Initialize the database and create tables if they don't exist."""
    conn = sqlite3.connect("tv_shows_reviews.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tv_shows (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            genre TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_id INTEGER NOT NULL,
            rating REAL NOT NULL,
            note TEXT,
            FOREIGN KEY (movie_id) REFERENCES tv_shows (id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()

#books
def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            genre VARCHAR(100),
            reviews_count INT DEFAULT 0
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INT AUTO_INCREMENT PRIMARY KEY,
            book_id INT NOT NULL,
            rating INT NOT NULL,
            note TEXT,
            FOREIGN KEY (book_id) REFERENCES books (id) ON DELETE CASCADE
        )
    ''')
    connection.commit()
    connection.close()

if __name__ == "__main__":
    initialize_db()
    initialize_tvshow_db()
