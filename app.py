import gradio as gr
import requests

# API Base URL
API_BASE_URL = "http://127.0.0.1:5000"

# Movie Functions

def add_movie(name):
    response = requests.post(f"{API_BASE_URL}/movies", json={"name": name})
    if response.status_code == 201:
        return response.json().get("message", "✅ Movie added successfully!")
    return f"❌ Error: {response.json().get('error', 'Unexpected error')}"

def view_movies():
    response = requests.get(f"{API_BASE_URL}/movies")
    if response.status_code == 200:
        movies = response.json()
        return "\n".join([f"ID: {movie['id']} | Name: {movie['name']}" for movie in movies])
    return "Failed to fetch movies."

def view_movie_reviews(movie_id):
    response = requests.get(f"{API_BASE_URL}/movies/{movie_id}/reviews")
    if response.status_code == 200:
        movie = response.json()
        reviews = movie.get("reviews", [])
        if reviews:
            return "\n".join(
                [f"Review ID: {review['review_id']} | Rating: {review['rating']} | Note: {review['note']}" for review in reviews]
            )
        return "No reviews found for this movie."
    return response.json().get("error", "Error fetching reviews.")

def add_movie_review(movie_id, rating, note):
    response = requests.post(f"{API_BASE_URL}/movies/{movie_id}/reviews", json={"rating": rating, "note": note})
    if response.status_code == 201:
        return response.json()["message"]
    return response.json()["error"]

def delete_movie(movie_id):
    response = requests.delete(f"{API_BASE_URL}/movies/{movie_id}")
    if response.status_code == 200:
        return response.json()["message"]
    return response.json()["error"]

def delete_movie_review(movie_id, review_id):
    response = requests.delete(f"{API_BASE_URL}/movies/{movie_id}/reviews/{review_id}")
    if response.status_code == 200:
        return response.json()["message"]
    return response.json()["error"]

# Book Functions

def add_book(title):
    response = requests.post(f"{API_BASE_URL}/books", json={"title": title})
    if response.status_code == 201:
        return response.json()["message"]
    return response.json()["error"]

def view_books():
    response = requests.get(f"{API_BASE_URL}/books")
    if response.status_code == 200:
        books = response.json()["books"]
        return "\n".join([f"ID: {book['id']} | Title: {book['title']}" for book in books])
    return "Failed to fetch books."

def view_book_reviews(book_id):
    response = requests.get(f"{API_BASE_URL}/books/{book_id}")
    if response.status_code == 200:
        book = response.json()
        reviews = book.get("reviews", [])
        if reviews:
            return "\n".join(
                [f"Review ID: {review['review_id']} | Rating: {review['rating']} | Note: {review['note']}" for review in reviews]
            )
        return "No reviews found for this book."
    return response.json().get("error", "Error fetching reviews.")

def add_book_review(book_id, rating, note):
    response = requests.post(f"{API_BASE_URL}/books/{book_id}/reviews", json={"rating": rating, "note": note})
    if response.status_code == 201:
        return response.json()["message"]
    return response.json()["error"]

def delete_book(book_id):
    response = requests.delete(f"{API_BASE_URL}/books/{book_id}")
    if response.status_code == 200:
        return response.json()["message"]
    return response.json()["error"]

def delete_book_review(book_id, review_id):
    response = requests.delete(f"{API_BASE_URL}/books/{book_id}")
    if response.status_code == 200:
        return response.json()["message"]
    return response.json()["error"]

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("# 🎥 Movie & 📚 Book Manager with Reviews")

    with gr.Tab("Movies"):
        
        # Add Movie
        with gr.Row():
            gr.Markdown("## Add a Movie")
            movie_name_input = gr.Textbox(label="Movie Name", placeholder="Enter movie name...")
            movie_add_button = gr.Button("Add Movie")
            movie_output = gr.Textbox(label="Status")
            movie_add_button.click(add_movie, inputs=movie_name_input, outputs=movie_output)

        # View Movies
        with gr.Row():
            gr.Markdown("## View Movies")
            view_movies_button = gr.Button("View Movies")
            movies_output = gr.Textbox(label="Movie List")
            view_movies_button.click(view_movies, outputs=movies_output)

        # Add Movie Review
        with gr.Row():
            movie_id_input = gr.Number(label="Movie ID", value=1)
            movie_rating_input = gr.Slider(label="Rating", minimum=1, maximum=5, step=0.5)
            movie_note_input = gr.Textbox(label="Review Note", placeholder="Write your review...")
            movie_review_button = gr.Button("Add Review")
            review_output = gr.Textbox(label="Status")
            movie_review_button.click(
                add_movie_review, inputs=[movie_id_input, movie_rating_input, movie_note_input], outputs=review_output
            )

        # View Movie Reviews
        with gr.Row():
            gr.Markdown("## View Reviews")
            view_reviews_movie_id_input = gr.Number(label="Movie ID", value=1)
            view_movie_reviews_button = gr.Button("View Reviews")
            movie_reviews_output = gr.Textbox(label="Movie Reviews")
            view_movie_reviews_button.click(
                view_movie_reviews, inputs=view_reviews_movie_id_input, outputs=movie_reviews_output
            )

        # Delete Movie
        with gr.Row():
            delete_movie_id_input = gr.Number(label="Movie ID to Delete", value=1)
            delete_movie_button = gr.Button("Delete Movie")
            delete_movie_output = gr.Textbox(label="Status")
            delete_movie_button.click(delete_movie, inputs=delete_movie_id_input, outputs=delete_movie_output)

        # Delete Movie Review
        with gr.Row():
            delete_movie_review_id_input = gr.Number(label="Movie ID", value=1)
            delete_review_id_input = gr.Number(label="Review ID to Delete", value=1)
            delete_review_button = gr.Button("Delete Review")
            delete_review_output = gr.Textbox(label="Status")
            delete_review_button.click(
                delete_movie_review, inputs=[delete_movie_review_id_input, delete_review_id_input], outputs=delete_review_output
            )

    with gr.Tab("Books"):
        
        # Add Book
        with gr.Row():
            gr.Markdown("## Add a Book")
            book_title_input = gr.Textbox(label="Book Tittle", placeholder="Enter book title...")
            book_add_button = gr.Button("Add Book")
            book_output = gr.Textbox(label="Status")
            book_add_button.click(add_book, inputs=book_title_input, outputs=book_output)

        # View Books
        with gr.Row():
            gr.Markdown("## View Books")
            view_books_button = gr.Button("View Books")
            books_output = gr.Textbox(label="Book List")
            view_books_button.click(view_books, outputs=books_output)

        # Add Book Review
        with gr.Row():
            book_id_input = gr.Number(label="Book ID", value=1)
            book_rating_input = gr.Slider(label="Rating", minimum=1, maximum=5, step=0.5)
            book_note_input = gr.Textbox(label="Review Note", placeholder="Write your review...")
            book_review_button = gr.Button("Add Review")
            review_output = gr.Textbox(label="Status")
            book_review_button.click(
                add_book_review, inputs=[book_id_input, book_rating_input, book_note_input], outputs=review_output
            )

        # View Book Reviews
        with gr.Row():
            gr.Markdown("## View Reviews")
            view_reviews_book_id_input = gr.Number(label="Book ID", value=1)
            view_book_reviews_button = gr.Button("View Reviews")
            book_reviews_output = gr.Textbox(label="Book Reviews")
            view_book_reviews_button.click(
                view_book_reviews, inputs=view_reviews_book_id_input, outputs=book_reviews_output
            )

        # Delete Book
        with gr.Row():
            delete_book_id_input = gr.Number(label="Book ID to Delete", value=1)
            delete_book_button = gr.Button("Delete Book")
            delete_book_output = gr.Textbox(label="Status")
            delete_book_button.click(delete_book, inputs=delete_book_id_input, outputs=delete_book_output)

        # Delete Book Review
        with gr.Row():
            delete_book_review_book_id_input = gr.Number(label="Book ID", value=1)
            delete_book_review_id_input = gr.Number(label="Review ID to Delete", value=1)
            delete_book_review_button = gr.Button("Delete Review")
            delete_book_review_output = gr.Textbox(label="Status")
            delete_book_review_button.click(
                delete_book_review, inputs=[delete_book_review_book_id_input, delete_book_review_id_input], outputs=delete_book_review_output
            )

if __name__ == "__main__":
    demo.launch()