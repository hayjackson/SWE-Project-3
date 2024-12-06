#Author: Mastewal


import sqlite3

DATABASE = 'tv_shows_reviews.db'

def add_show(title, genre):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tv_shows (title, genre) VALUES (?, ?)', (title, genre))
    conn.commit()
    conn.close()
    return {"message": f"TV Show '{title}' added successfully."}

def add_review(tv_show_id, rating, note):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO reviews (tv_show_id, rating, note) VALUES (?, ?, ?)', (tv_show_id, rating, note))
    conn.commit()
    conn.close()
    return {"message": f"Review added to TV Show ID {tv_show_id}."}

def edit_review(tv_show_id, review_id, rating=None, note=None):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    if rating:
        cursor.execute('UPDATE reviews SET rating = ? WHERE id = ? AND tv_show_id = ?', (rating, review_id, tv_show_id))
    if note:
        cursor.execute('UPDATE reviews SET note = ? WHERE id = ? AND tv_show_id = ?', (note, review_id, tv_show_id))
    conn.commit()
    conn.close()
    return {"message": f"Review ID {review_id} for TV Show ID {tv_show_id} updated."}

def delete_review(tv_show_id, review_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM reviews WHERE id = ? AND tv_show_id = ?', (review_id, tv_show_id))
    conn.commit()
    conn.close()
    return {"message": f"Review ID {review_id} deleted from TV Show ID {tv_show_id}."}

def delete_show(tv_show_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM reviews WHERE tv_show_id = ?', (tv_show_id,))
    cursor.execute('DELETE FROM tv_shows WHERE id = ?', (tv_show_id,))
    conn.commit()
    conn.close()
    return {"message": f"TV Show ID {tv_show_id} and its reviews have been deleted."}

def view_reviews():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tv_shows')
    tv_shows = cursor.fetchall()
    result = []
    for tv_show in tv_shows:
        cursor.execute('SELECT * FROM reviews WHERE tv_show_id = ?', (tv_show[0],))
        reviews = cursor.fetchall()
        result.append({
            "id": tv_show[0],
            "title": tv_show[1],
            "genre": tv_show[2],
            "reviews": [{"review_id": r[0], "rating": r[2], "note": r[3]} for r in reviews]
        })
    conn.close()
    return result

def search_reviews(tv_show_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tv_shows WHERE id = ?', (tv_show_id,))
    tv_show = cursor.fetchone()
    if not tv_show:
        return {"error": "TV Show not found."}
    cursor.execute('SELECT * FROM reviews WHERE tv_show_id = ?', (tv_show_id,))
    reviews = cursor.fetchall()
    conn.close()
    return {
        "id": tv_show[0],
        "title": tv_show[1],
        "genre": tv_show[2],
        "reviews": [{"review_id": r[0], "rating": r[2], "note": r[3]} for r in reviews]
    }

def search_by_genre(genre):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tv_shows WHERE genre = ?', (genre,))
    tv_shows = cursor.fetchall()
    conn.close()
    return [{"id": tv_show[0], "title": tv_show[1], "genre": tv_show[2]} for tv_show in tv_shows]
