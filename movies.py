# Core Backend Functioning of movie tab of the review app
# Author: Aditi Jha
# Date: November 01, 2024

import json
import os

# JSON file to store data
DATABASE_FILE = 'movie_reviews.json'

# Loading data from the JSON file
def load_data():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'r') as file:
            return json.load(file)
    return {"movies": []}

# Saving data to the JSON file
def save_data(data):
    with open(DATABASE_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Adding a new movie
def add_movie(movie_name):
    data = load_data()
    movie = {
        "id": len(data["movies"]) + 1,
        "name": movie_name,
        "reviews": []
    }
    data["movies"].append(movie)
    save_data(data)
    print(f"Movie '{movie_name}' added successfully.")

# Adding a review to a movie
def add_review(movie_id, rating, note):
    data = load_data()
    for movie in data["movies"]:
        if movie["id"] == movie_id:
            review_id = len(movie["reviews"]) + 1
            review = {
                "review_id": review_id,
                "rating": rating,
                "note": note
            }
            movie["reviews"].append(review)
            save_data(data)
            print(f"Review added to movie ID {movie_id}.")
            return
    print("Movie not found.")

# Editing an existing review
def edit_review(movie_id, review_id, rating=None, note=None):
    data = load_data()
    for movie in data["movies"]:
        if movie["id"] == movie_id:
            for review in movie["reviews"]:
                if review["review_id"] == review_id:
                    if rating is not None:
                        review["rating"] = rating
                    if note is not None:
                        review["note"] = note
                    save_data(data)
                    print(f"Review ID {review_id} for movie ID {movie_id} updated.")
                    return
            print("Review not found.")
            return
    print("Movie not found.")

# Deleting a review
def delete_review(movie_id, review_id):
    data = load_data()
    for movie in data["movies"]:
        if movie["id"] == movie_id:
            movie["reviews"] = [review for review in movie["reviews"] if review["review_id"] != review_id]
            save_data(data)
            print(f"Review ID {review_id} deleted from movie ID {movie_id}.")
            return
    print("Movie or review not found.")


# Deleting a movie and its associated reviews
def delete_movie(movie_id):
    data = load_data()
    # Filter out the movie to delete
    data["movies"] = [movie for movie in data["movies"] if movie["id"] != movie_id]
    save_data(data)
    print(f"Movie ID {movie_id} and its reviews have been deleted.")


# Viewing all reviews
def view_reviews():
    data = load_data()
    for movie in data["movies"]:
        print(f"Movie ID: {movie['id']} - Name: {movie['name']}")
        for review in movie["reviews"]:
            print(f"  Review ID: {review['review_id']} | Rating: {review['rating']} | Note: {review['note']}")

# Searching and filter reviews by movie ID
def search_reviews(movie_id):
    data = load_data()
    for movie in data["movies"]:
        if movie["id"] == movie_id:
            print(f"Movie ID: {movie['id']} - Name: {movie['name']}")
            for review in movie["reviews"]:
                print(f"  Review ID: {review['review_id']} | Rating: {review['rating']} | Note: {review['note']}")
            return
    print("Movie not found.")

