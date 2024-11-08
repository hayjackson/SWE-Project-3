# books.py
import json
import os

DATABASE_FILE = 'book_reviews.json'

def load_data():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'r') as file:
            return json.load(file)
    return {"books": []}

def save_data(data):
    with open(DATABASE_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def add_book(book_title):
    data = load_data()
    book = {
        "id": len(data["books"]) + 1,
        "title": book_title,
        "reviews": []
    }
    data["books"].append(book)
    save_data(data)
    return book  # Return the book dictionary for API responses

def add_review(book_id, rating, note):
    data = load_data()
    for book in data["books"]:
        if book["id"] == book_id:
            review_id = len(book["reviews"]) + 1
            review = {
                "review_id": review_id,
                "rating": rating,
                "note": note
            }
            book["reviews"].append(review)
            save_data(data)
            return review
    return None  # Return None if book not found

def get_book(book_id):
    data = load_data()
    for book in data["books"]:
        if book["id"] == book_id:
            return book
    return None

def delete_book(book_id):
    data = load_data()
    original_count = len(data["books"])
    data["books"] = [book for book in data["books"] if book["id"] != book_id]
    if len(data["books"]) < original_count:
        save_data(data)
        return True
    return False
def load_data():
    try:
        with open(DATABASE_FILE, 'r') as file:
            return json.load(file) 
    except FileNotFoundError:
        return {"books": []}
    except json.JSONDecodeError:
        return {"books": []}

def save_data(data):
    try:
        with open(DATABASE_FILE, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error saving data: {e}")

def add_book(book_title):
    data = load_data()
    book_id = len(data["books"]) + 1
    book = {
        "id": book_id,
        "title": book_title,
        "reviews": []
    }
    data["books"].append(book)
    save_data(data)
    return book

def add_review(book_id, rating, note):
    data = load_data()
    for book in data["books"]:
        if book["id"] == book_id:
            review_id = len(book["reviews"]) + 1
            review = {
                "review_id": review_id,
                "rating": rating,
                "note": note
            }
            book["reviews"].append(review)
            save_data(data)
            return review
    return None

def get_book(book_id):
    data = load_data()
    for book in data["books"]:
        if book["id"] == book_id:
            return book
    return None

def delete_book(book_id):
    data = load_data()
    original_count = len(data["books"])
    data["books"] = [book for book in data["books"] if book["id"] != book_id]
    if len(data["books"]) < original_count:
        save_data(data)
        return True
    return False

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
                if review["review_id"] == review_id:
                    review["rating"] = rating
                    review["note"] = note
                    save_data(data)
                    return True
    return False

def delete_review(book_id, review_id):
    data = load_data()
    for book in data["books"]:
        if book["id"] == book_id:
            original_count = len(book["reviews"])
            book["reviews"] = [review for review in book["reviews"] if review["review_id"] != review_id]
            if len(book["reviews"]) < original_count:
                save_data(data)
                return True
    return False