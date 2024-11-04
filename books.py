# Book Tab of the review app
# Author: Kai Francis

import json
import os

# JSON file to store data
DATABASE_FILE = 'book_reviews.json'

# Loading data from the JSON file
def load_data():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'r') as file:
            return json.load(file)
    return {"books": []}

# Saving data to the JSON file
def save_data(data):
    with open(DATABASE_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Adding a new book
def add_book(book_title):
    data = load_data()
    book = {
        "id": len(data["books"]) + 1,
        "title": book_title,
        "reviews": []
    }
    data["books"].append(book)
    save_data(data)
    print(f"Book '{book_title}' added successfully.")

# Adding a review to a book
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
            print(f"Review added to book ID {book_id}.")
            return
    print("Book not found.")

# Editing an existing review
def edit_review(book_id, review_id, rating=None, note=None):
    data = load_data()
    for book in data["books"]:
        if book["id"] == book_id:
            for review in book["reviews"]:
                if review["review_id"] == review_id:
                    if rating is not None:
                        review["rating"] = rating
                    if note is not None:
                        review["note"] = note
                    save_data(data)
                    print(f"Review ID {review_id} for book ID {book_id} updated.")
                    return
            print("Review not found.")
            return
    print("Book not found.")

# Deleting a review
def delete_review(book_id, review_id):
    data = load_data()
    for book in data["books"]:
        if book["id"] == book_id:
            book["reviews"] = [review for review in book["reviews"] if review["review_id"] != review_id]
            save_data(data)
            print(f"Review ID {review_id} deleted from book ID {book_id}.")
            return
    print("Book or review not found.")

# Deleting a book and its associated reviews
def delete_book(book_id):
    data = load_data()
    # Filter out the book to delete
    data["books"] = [book for book in data["books"] if book["id"] != book_id]
    save_data(data)
    print(f"Book ID {book_id} and its reviews have been deleted.")

# Viewing all reviews
def view_reviews():
    data = load_data()
    for book in data["books"]:
        print(f"Book ID: {book['id']} - Title: {book['title']}")
        for review in book["reviews"]:
            print(f"  Review ID: {review['review_id']} | Rating: {review['rating']} | Note: {review['note']}")

# Searching and filtering reviews by book ID
def search_reviews(book_id):
    data = load_data()
    for book in data["books"]:
        if book["id"] == book_id:
            print(f"Book ID: {book['id']} - Title: {book['title']}")
            for review in book["reviews"]:
                print(f"  Review ID: {review['review_id']} | Rating: {review['rating']} | Note: {review['note']}")
            return
    print("Book not found.")
