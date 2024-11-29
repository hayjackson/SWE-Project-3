# Book Tab of the review app
# Author: Kai Francis

import sqlite3

DATABASE = 'books.db'

def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row  # Allows accessing rows like dictionaries
    return connection

# Create tables if they do not exist
def initialize_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create books table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            genre TEXT,
            reviews_count INTEGER DEFAULT 0
        )
    ''')

    # Create reviews table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            rating INTEGER NOT NULL,
            note TEXT,
            FOREIGN KEY (book_id) REFERENCES books (id)
        )
    ''')
    conn.commit()
    conn.close()

# Add a new book
def add_book(book_title, genre):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO books (title, genre) VALUES (?, ?)",
        (book_title, genre)
    )
    conn.commit()
    book_id = cursor.lastrowid
    conn.close()
    return {"id": book_id, "title": book_title, "genre": genre}

# Add a review to a book
def add_review(book_id, rating, note):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO reviews (book_id, rating, note) VALUES (?, ?, ?)",
        (book_id, rating, note)
    )
    # Update the reviews_count in the books table
    cursor.execute(
        "UPDATE books SET reviews_count = reviews_count + 1 WHERE id = ?",
        (book_id,)
    )
    conn.commit()
    conn.close()
    return {"book_id": book_id, "rating": rating, "note": note}

# Retrieve a specific book
def get_book(book_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    book = cursor.fetchone()
    conn.close()
    return dict(book) if book else None

# Filter books by genre
def filter_books_by_genre(genre):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM books WHERE LOWER(genre) LIKE ?",
        (f"%{genre.lower()}%",)
    )
    books = cursor.fetchall()
    conn.close()
    return [dict(book) for book in books]

# Delete a book and its reviews
def delete_book(book_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reviews WHERE book_id = ?", (book_id,))
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()
    return {"message": f"Book with ID {book_id} deleted"}

def update_book(book_id, book_title):
    data = load_data()
    for book in data["books"]:
        if book["id"] == book_id:
            book["title"] = book_title
            save_data(data)
            return True
    return False

def update_review(book_id, review_id, rating, note):
    data = load_data()
    for book in data["books"]:
        if book["id"] == book_id:
            for review in book["reviews"]:
                print(f"  Review ID: {review['review_id']} | Rating: {review['rating']} | Note: {review['note']}")
            return
    print("Book not found.")

def add_review_to_db(book_id, rating, note):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO reviews (book_id, rating, note) VALUES (?, ?, ?)",
        (book_id, rating, note)
    )
    # Optionally, update the reviews_count in books
    cursor.execute(
        "UPDATE books SET reviews_count = reviews_count + 1 WHERE id = ?",
        (book_id,)
    )
    conn.commit()
    conn.close()
    return {"message": "Review added successfully"}


# Initialize the database when the script runs
if __name__ == "__main__":
    initialize_database()



