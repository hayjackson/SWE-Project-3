#app.py
# GET /api/books: Retrieves a list of all books.
# GET /api/books/<int:book_id>: Retrieves a single book by its ID.
# POST /api/books: Creates a new book. Expects a JSON body with a "title" field.
# POST /api/books/<int:book_id>/reviews: Adds a review to a specified book by ID. Expects a JSON body with "rating" and "note" fields.
# DELETE /api/books/<int:book_id>: Deletes a book by ID.
from flask import Flask, jsonify, request
from books import add_book, add_review, get_book, delete_book, load_data

app = Flask(__name__)

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

#run the app
if __name__ == '__main__':
    app.run(debug=True)