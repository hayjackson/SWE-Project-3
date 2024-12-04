# Core Backend Functioning of movie tab of the review app
# Author: Aditi Jha
# Date: November 01, 2024, updated november 22, 2024, updated December 1, 2024

import sqlite3

DATABASE = 'movie_reviews.db'

def add_movie(name, genre):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO movies (name, genre) VALUES (?, ?)', (name, genre))
    conn.commit()
    conn.close()
    return {"message": f"Movie '{name}' added successfully."}

def add_review(movie_id, rating, note):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO reviews (movie_id, rating, note) VALUES (?, ?, ?)', (movie_id, rating, note))
    conn.commit()
    conn.close()
    return {"message": f"Review added to movie ID {movie_id}."}

def edit_review(movie_id, review_id, rating=None, note=None):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    if rating:
        cursor.execute('UPDATE reviews SET rating = ? WHERE id = ? AND movie_id = ?', (rating, review_id, movie_id))
    if note:
        cursor.execute('UPDATE reviews SET note = ? WHERE id = ? AND movie_id = ?', (note, review_id, movie_id))
    conn.commit()
    conn.close()
    return {"message": f"Review ID {review_id} for movie ID {movie_id} updated."}

def delete_review(movie_id, review_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM reviews WHERE id = ? AND movie_id = ?', (review_id, movie_id))
    conn.commit()
    conn.close()
    return {"message": f"Review ID {review_id} deleted from movie ID {movie_id}."}

def delete_movie(movie_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM reviews WHERE movie_id = ?', (movie_id,))
    cursor.execute('DELETE FROM movies WHERE id = ?', (movie_id,))
    conn.commit()
    conn.close()
    return {"message": f"Movie ID {movie_id} and its reviews have been deleted."}

def view_reviews():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM movies')
    movies = cursor.fetchall()
    result = []
    for movie in movies:
        cursor.execute('SELECT * FROM reviews WHERE movie_id = ?', (movie[0],))
        reviews = cursor.fetchall()
        result.append({
            "id": movie[0],
            "name": movie[1],
            "genre": movie[2],
            "reviews": [{"review_id": r[0], "rating": r[2], "note": r[3]} for r in reviews]
        })
    conn.close()
    return result

def search_reviews(movie_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM movies WHERE id = ?', (movie_id,))
    movie = cursor.fetchone()
    if not movie:
        return {"error": "Movie not found."}
    cursor.execute('SELECT * FROM reviews WHERE movie_id = ?', (movie_id,))
    reviews = cursor.fetchall()
    conn.close()
    return {
        "id": movie[0],
        "name": movie[1],
        "genre": movie[2],
        "reviews": [{"review_id": r[0], "rating": r[2], "note": r[3]} for r in reviews]
    }

def search_by_genre(genre):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM movies WHERE genre = ?', (genre,))
    movies = cursor.fetchall()
    conn.close()
    return [{"id": movie[0], "name": movie[1], "genre": movie[2]} for movie in movies]




#Keith


def view_movie_genre():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT genre FROM movies')
    genres = cursor.fetchall()
    result = [genre[0] for genre in genres]
    conn.close()
    return result


def view_top_movies():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM reviews ORDER BY rating DESC LIMIT 3')
    reviews = cursor.fetchall()
    result = [review[0] for review in reviews]
    conn.close()
    return result
