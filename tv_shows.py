# #Author Mastewal 
# TV_shows

import sqlite3

DATABASE = 'tv_shows_reviews.db'

def add_show(title, genre):
    """Add a new TV show."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tv_shows (title, genre) VALUES (?, ?)', (title, genre))
    conn.commit()
    conn.close()
    return {"message": f"TV Show '{title}' added successfully."}

def add_review(show_id, rating, note):
    """Add a review for a specific TV show."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    
    cursor.execute('SELECT id FROM tv_shows WHERE id = ?', (show_id,))
    if not cursor.fetchone():
        conn.close()
        return {"error": f"TV Show ID {show_id} does not exist."}

  
    cursor.execute('INSERT INTO reviews (movie_id, rating, note) VALUES (?, ?, ?)', (show_id, rating, note))
    conn.commit()
    conn.close()

    return {"message": f"Review added to TV Show ID {show_id}."}


def edit_review(show_id, review_id, rating=None, note=None):
    """Edit an existing review for a specific TV show."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    if rating is None and note is None:
        conn.close()
        return {"error": "No fields to update. Provide at least one of 'rating' or 'note'."}

    if rating is not None:
        cursor.execute(
            'UPDATE reviews SET rating = ? WHERE id = ? AND movie_id = ?',
            (rating, review_id, show_id)
        )

    if note is not None:
        cursor.execute(
            'UPDATE reviews SET note = ? WHERE id = ? AND movie_id = ?',
            (note, review_id, show_id)
        )

    conn.commit()
    conn.close()

    return {"message": f"Review ID {review_id} for TV Show ID {show_id} updated."}

def delete_review(show_id, review_id):
    """Delete a specific review from a TV show."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM reviews WHERE id = ? AND movie_id = ?', (review_id, show_id))
    
    conn.commit()
    conn.close()
    
    return {"message": f"Review ID {review_id} deleted from TV Show ID {show_id}."}

def delete_show(show_id):
    """Delete a TV show and all its associated reviews."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Delete all reviews associated with the show
    cursor.execute('DELETE FROM reviews WHERE movie_id = ?', (show_id,))
    
    # Delete the show itself
    cursor.execute('DELETE FROM tv_shows WHERE id = ?', (show_id,))
    
    conn.commit()
    conn.close()
    
    return {"message": f"TV Show ID {show_id} and its reviews have been deleted."}

def view_reviews():
    """View all TV shows along with their reviews."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Calculate average rating for each TV show
    cursor.execute('''
        SELECT tv_shows.id, tv_shows.title, tv_shows.genre, 
               IFNULL(AVG(reviews.rating), 0) as avg_rating
        FROM tv_shows
        LEFT JOIN reviews ON tv_shows.id = reviews.movie_id
        GROUP BY tv_shows.id
    ''')
    shows = cursor.fetchall()

    result = []

    for show in shows:
        cursor.execute('SELECT id, rating, note FROM reviews WHERE movie_id = ?', (show[0],))
        reviews = cursor.fetchall()

        result.append({
            "id": show[0],
            "title": show[1],
            "genre": show[2],
            "rating": show[3],  # Correct average rating
            "reviews": [{"review_id": r[0], "rating": r[1], "note": r[2]} for r in reviews]
        })

    conn.close()

    return result





def search_reviews(show_id):
    """Search for reviews of a specific TV show."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM tv_shows WHERE id = ?', (show_id,))
    
    show = cursor.fetchone()
    
    if not show:
        return {"error": "TV Show not found."}
    
    cursor.execute('SELECT * FROM reviews WHERE movie_id = ?', (show_id,))
    
    reviews = cursor.fetchall()
    
    conn.close()
    
    return {
        "id": show[0],
        "title": show[1],
        "genre": show[2],
        "reviews": [{"review_id": r[0], "rating": r[2], "note": r[3]} for r in reviews]
    }

def search_by_genre(genre):
    """Search for TV shows by genre."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    
    cursor.execute('SELECT id, title, genre, rating FROM tv_shows WHERE genre = ?', (genre,))
    shows = cursor.fetchall()
    
    conn.close()

  
    return [{"id": show[0], "title": show[1], "genre": show[2], "rating": show[3]} for show in shows]


