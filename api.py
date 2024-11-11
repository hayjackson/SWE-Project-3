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

#endpoint to get all books
@app.route('/books', methods=['GET'])
def get_books():
    logging.info('Getting all books')
    data = load_data()
    logging.info('Returning all books')
    return jsonify(data), 200

#endpoint to add a new book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_single_book(book_id):
    logging.info(f'Getting book with ID {book_id}')
    book = get_book(book_id)
    if book:
        logging.info(f'Returning book with ID {book_id}')
        return jsonify(book), 200
    logging.error(f'Book with ID {book_id} not found')
    return jsonify({"error": "Book not found"}), 404

#endpoint to create a new book
@app.route('/books', methods=['POST'])
def create_book():
    logging.info('Creating new book')
    book_data = request.json
    title = book_data.get('title')
    if title:
        logging.info(f'Adding book with title {title}')
        new_book = add_book(title)
        logging.info(f'Book with title {title} added')
        return jsonify(new_book), 201
    logging.error('Title is required')
    return jsonify({"error": "Title is required"}), 400

#endpoint to add a new review
@app.route('/books/<int:book_id>/reviews', methods=['POST'])
def create_book_review(book_id):
    logging.info(f'Adding review to book with ID {book_id}')
    review_data = request.json
    rating = review_data.get('rating')
    note = review_data.get('note')
    if rating is not None and note is not None:
        logging.info(f'Adding review with rating {rating} and note {note} to book with ID {book_id}')
        new_review = add_review(book_id, rating, note)
        if new_review:
            logging.info(f'Review added to book with ID {book_id}')
            return jsonify(new_review), 201
        logging.error(f'Book with ID {book_id} not found')
        return jsonify({"error": "Book not found"}), 404
    logging.error('Rating and note are required')
    return jsonify({"error": "Rating and note are required"}), 400

#endpoint to delete a book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_single_book(book_id):
    logging.info(f'Deleting book with ID {book_id}')
    success = delete_book(book_id)
    if success:
        logging.info(f'Book with ID {book_id} deleted')
        return jsonify({"message": f"Book ID {book_id} deleted"}), 200
    logging.error(f'Book with ID {book_id} not found')
    return jsonify({"error

#endpoint to get all books
@app.route('/books', methods=['GET'])
def get_books():
    data = load_data()
    return jsonify(data), 200

#endpoint to add a new book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_single_book(book_id):
    book = get_book(book_id)
    if book:
        return jsonify(book), 200
    return jsonify({"error": "Book not found"}), 404

#endpoint to create a new book
@app.route('/books', methods=['POST'])
def create_book():
    book_data = request.json
    title = book_data.get('title')
    if title:
        new_book = add_book(title)
        return jsonify(new_book), 201
    return jsonify({"error": "Title is required"}), 400

#endpoint to add a new review
@app.route('/books/<int:book_id>/reviews', methods=['POST'])
def create_book_review(book_id):
    review_data = request.json
    rating = review_data.get('rating')
    note = review_data.get('note')
    if rating is not None and note is not None:
        new_review = add_review(book_id, rating, note)
        if new_review:
            return jsonify(new_review), 201
        return jsonify({"error": "Book not found"}), 404
    return jsonify({"error": "Rating and note are required"}), 400

#endpoint to delete a book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_single_book(book_id):
    success = delete_book(book_id)
    if success:
        return jsonify({"message": f"Book ID {book_id} deleted"}), 200
    return jsonify({"error": "Book not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
