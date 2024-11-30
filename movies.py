# Core Backend Functioning of movie tab of the review app
# Author: Aditi Jha
# Date: November 01, 2024, updated november 22, 2024

from movies_db import get_connection

# Adding a new movie with genre
def add_movie(movie_name, genre):
    connection = get_connection()
    cursor = connection.cursor()
    query = "INSERT INTO movies (name, genre) VALUES (%s, %s)"
    cursor.execute(query, (movie_name, genre))
    connection.commit()
    movie_id = cursor.lastrowid
    connection.close()
    return {"message": f"Movie '{movie_name}' added successfully.", "movie": {"id": movie_id, "name": movie_name, "genre": genre}}

# Adding a review to a movie
def add_review(movie_id, rating, note):
    connection = get_connection()
    cursor = connection.cursor()
    query = "INSERT INTO reviews (movie_id, rating, note) VALUES (%s, %s, %s)"
    cursor.execute(query, (movie_id, rating, note))
    connection.commit()
    review_id = cursor.lastrowid
    connection.close()
    return {"message": f"Review added to movie ID {movie_id}.", "review": {"review_id": review_id, "rating": rating, "note": note}}

# Editing a review
def edit_review(movie_id, review_id, rating=None, note=None):
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
    values.extend([movie_id, review_id])

    query = f"UPDATE reviews SET {', '.join(updates)} WHERE movie_id = %s AND id = %s"
    cursor.execute(query, tuple(values))
    connection.commit()
    connection.close()
    return {"message": f"Review ID {review_id} for movie ID {movie_id} updated."}

# Deleting a review
def delete_review(movie_id, review_id):
    connection = get_connection()
    cursor = connection.cursor()
    query = "DELETE FROM reviews WHERE movie_id = %s AND id = %s"
    cursor.execute(query, (movie_id, review_id))
    connection.commit()
    connection.close()
    return {"message": f"Review ID {review_id} deleted from movie ID {movie_id}."}

# Deleting a movie
def delete_movie(movie_id):
    connection = get_connection()
    cursor = connection.cursor()
    query = "DELETE FROM movies WHERE id = %s"
    cursor.execute(query, (movie_id,))
    connection.commit()
    connection.close()
    return {"message": f"Movie ID {movie_id} and its reviews have been deleted."}

# Viewing all movies
def view_movies():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM movies"
    cursor.execute(query)
    movies = cursor.fetchall()
    connection.close()
    return movies

# Searching movies by genre
def search_movies_by_genre(genre):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM movies WHERE genre = %s"
    cursor.execute(query, (genre,))
    movies = cursor.fetchall()
    connection.close()
    return movies
