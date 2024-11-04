# Author: Aditi Jha, November 4, 2024
# Implementing REST API for my movie tab for our review app.

from flask import Flask, jsonify, request
import movies  # Importing the existing functions, Aditi Jha, 11/04/2024

app = Flask(__name__)

# Endpoint to add a movie, Aditi Jha, 11/04/2024
@app.route('/movies', methods=['POST'])
def add_movie():
    data = request.get_json()
    movie_name = data.get("name")
    if movie_name:
        movies.add_movie(movie_name)
        return jsonify({"message": f"Movie '{movie_name}' added successfully."}), 201
    else:
        return jsonify({"error": "Movie name is required"}), 400

# Endpoint to add a review to a movie, Aditi Jha, 11/04/2024
@app.route('/movies/<int:movie_id>/reviews', methods=['POST'])
def add_review(movie_id):
    data = request.get_json()
    rating = data.get("rating")
    note = data.get("note")
    if rating is not None and note:
        movies.add_review(movie_id, rating, note)
        return jsonify({"message": f"Review added to movie ID {movie_id}."}), 201
    else:
        return jsonify({"error": "Rating and note are required"}), 400

# Endpoint to edit a review, Aditi Jha, 11/04/2024
@app.route('/movies/<int:movie_id>/reviews/<int:review_id>', methods=['PUT'])
def edit_review(movie_id, review_id):
    data = request.get_json()
    rating = data.get("rating")
    note = data.get("note")
    movies.edit_review(movie_id, review_id, rating, note)
    return jsonify({"message": f"Review ID {review_id} for movie ID {movie_id} updated."})

# Endpoint to delete a review, Aditi Jha, 11/04/2024
@app.route('/movies/<int:movie_id>/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(movie_id, review_id):
    movies.delete_review(movie_id, review_id)
    return jsonify({"message": f"Review ID {review_id} deleted from movie ID {movie_id}."})

# Endpoint to delete a movie, Aditi Jha, 11/04/2024
@app.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    movies.delete_movie(movie_id)
    return jsonify({"message": f"Movie ID {movie_id} and its reviews have been deleted."})

# Endpoint to view all reviews, Aditi Jha, 11/04/2024
@app.route('/movies', methods=['GET'])
def view_reviews():
    all_reviews = movies.load_data()["movies"]
    return jsonify(all_reviews)

# Endpoint to search for reviews by movie ID, Aditi Jha, 11/04/2024
@app.route('/movies/<int:movie_id>/reviews', methods=['GET'])
def search_reviews(movie_id):
    data = movies.load_data()
    for movie in data["movies"]:
        if movie["id"] == movie_id:
            return jsonify(movie)
    return jsonify({"error": "Movie not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
