# Core Backend Functioning of book tab of the review app
# Author: Kai Francis
# Date: Updated December 2, 2024

import sqlite3

DATABASE = 'books.db'

# Adding a new book with genre
def add_book(book_title, genre):
    connection = get_connection()
    cursor = connection.cursor()
    query = "INSERT INTO books (title, genre) VALUES (%s, %s)"
    cursor.execute(query, (book_title, genre))
    connection.commit()
    book_id = cursor.lastrowid
    connection.close()
    return {"message": f"Book '{book_title}' added successfully.", "book": {"id": book_id, "title": book_title, "genre": genre}}

# Adding a review to a book
def add_review(book_id, rating, note):
    connection = get_connection()
    cursor = connection.cursor()
    query = "INSERT INTO reviews (book_id, rating, note) VALUES (%s, %s, %s)"
    cursor.execute(query, (book_id, rating, note))
    # Optionally update the reviews_count in books
    update_query = "UPDATE books SET reviews_count = reviews_count + 1 WHERE id = %s"
    cursor.execute(update_query, (book_id,))
    connection.commit()
    review_id = cursor.lastrowid
    connection.close()
    return {"message": f"Review added to book ID {book_id}.", "review": {"review_id": review_id, "rating": rating, "note": note}}

# Editing a review
def edit_review(book_id, review_id, rating=None, note=None):
    connection = get_connection()
    cursor = connection.cursor()
    updates = []
    values = []

    if rating is not None:
        updates.append("rating = %s")
        values.append(rating)
    if note is not None:
        updates.append("note = %s")
        values.append(note)
    values.extend([book_id, review_id])

    query = f"UPDATE reviews SET {', '.join(updates)} WHERE book_id = %s AND id = %s"
    cursor.execute(query, tuple(values))
    connection.commit()
    connection.close()
    return {"message": f"Review ID {review_id} for book ID {book_id} updated."}

# Deleting a review
def delete_review(book_id, review_id):
    connection = get_connection()
    cursor = connection.cursor()
    query = "DELETE FROM reviews WHERE book_id = %s AND id = %s"
    cursor.execute(query, (book_id, review_id))
    connection.commit()
    connection.close()
    return {"message": f"Review ID {review_id} deleted from book ID {book_id}."}

# Deleting a book
def delete_book(book_id):
    connection = get_connection()
    cursor = connection.cursor()
    query = "DELETE FROM reviews WHERE book_id = %s"
    cursor.execute(query, (book_id,))
    delete_book_query = "DELETE FROM books WHERE id = %s"
    cursor.execute(delete_book_query, (book_id,))
    connection.commit()
    connection.close()
    return {"message": f"Book ID {book_id} and its reviews have been deleted."}

# Viewing all books
def view_books():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM books"
    cursor.execute(query)
    books = cursor.fetchall()
    connection.close()
    return books

# Searching books by genre
def search_books_by_genre(genre):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM books WHERE LOWER(genre) LIKE %s"
    cursor.execute(query, (f"%{genre.lower()}%",))
    books = cursor.fetchall()
    connection.close()
    return books

# Searching a book by ID
def search_book_by_id(book_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM books WHERE id = %s"
    cursor.execute(query, (book_id,))
    book = cursor.fetchone()
    connection.close()
    if book:
        return {"message": "Book found.", "book": book}
    return {"error": f"Book with ID {book_id} not found."}


# Run initialization when the script is executed
if __name__ == "__main__":
    initialize_database()
