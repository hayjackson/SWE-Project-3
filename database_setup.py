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
    conn = sqlite3.connect('tvshows_rvw.db')
    cursor = conn.cursor()

    # Creating tv_shows 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tv_shows (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            genre TEXT NOT NULL,
            rating REAL
        )
    ''')

    conn.commit()
    conn.close()
 

if __name__ == "__main__":
    initialize_db()
