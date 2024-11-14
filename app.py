import gradio as gr
import requests

# Base URL of the Flask API
BASE_URL = "http://127.0.0.1:5000"

# Functions to interact with the API

# Add a movie
def add_movie_frontend(movie_name):
    if not movie_name.strip():
        return "❌ Error: Movie name cannot be empty!"
    try:
        response = requests.post(f"{BASE_URL}/movies", json={"name": movie_name})
        if response.status_code == 201:
            return response.json().get("message", "✅ Movie added successfully!")
        return f"❌ Error: {response.json().get('error', 'Unexpected error')}"
    except requests.exceptions.RequestException as e:
        return f"❌ Error: Failed to connect to the API - {str(e)}"

# Add a review to a movie
def add_movie_review(movie_id, rating, note):
    if not movie_id.isdigit():
        return "❌ Error: Movie ID must be an integer!"
    if not (0 <= float(rating) <= 5):
        return "❌ Error: Rating must be between 0 and 5!"
    if not note.strip():
        return "❌ Error: Review note cannot be empty!"
    try:
        response = requests.post(
            f"{BASE_URL}/movies/{movie_id}/reviews",
            json={"rating": float(rating), "note": note},
        )
        if response.status_code == 201:
            return response.json().get("message", "✅ Review added successfully!")
        return f"❌ Error: {response.json().get('error', 'Unexpected error')}"
    except requests.exceptions.RequestException as e:
        return f"❌ Error: Failed to connect to the API - {str(e)}"

# View all movies and their reviews
def view_movies():
    try:
        response = requests.get(f"{BASE_URL}/movies")
        if response.status_code == 200:
            movies = response.json()
            if not movies:
                return "🎥 Your movie list is empty. Add some movies to get started!"
            output = ["🎥 Movie List:"]
            for movie in movies:
                output.append(f"Movie #{movie['id']}: {movie['name']}")
                if not movie["reviews"]:
                    output.append("   No reviews yet.")
                else:
                    for review in movie["reviews"]:
                        output.append(
                            f"   Review #{review['review_id']} | Rating: {review['rating']}/5 | {review['note']}"
                        )
            return "\n".join(output)
        return f"❌ Error: {response.json().get('error', 'Unexpected error')}"
    except requests.exceptions.RequestException as e:
        return f"❌ Error: Failed to connect to the API - {str(e)}"
# Delete a movie
def delete_movie(movie_id):
    if not movie_id.isdigit():
        return "❌ Error: movie ID must be an integer!"
    try:
        response = requests.delete(f"{BASE_URL}/movies/{book_id}")
        if response.status_code == 200:
            return response.json().get("message", "✅ Movie deleted successfully!")
        return f"❌ Error: {response.json().get('error', 'Unexpected error')}"
    except requests.exceptions.RequestException as e:
        return f"❌ Error: Failed to connect to the API - {str(e)}"

# Delete a review for a movie
def delete_movie_review(movie_id, review_id):
    if not movie_id.isdigit() or not review_id.isdigit():
        return "❌ Error: Both movie ID and Review ID must be integers!"
    try:
        response = requests.delete(f"{BASE_URL}/movies/{book_id}/reviews/{review_id}")
        if response.status_code == 200:
            return response.json().get("message", "✅ Review deleted successfully!")
        return f"❌ Error: {response.json().get('error', 'Unexpected error')}"
    except requests.exceptions.RequestException as e:
        return f"❌ Error: Failed to connect to the API - {str(e)}"


# Add a book
def add_book_frontend(book_title):
    if not book_title.strip():
        return "❌ Error: Book title cannot be empty!"
    try:
        response = requests.post(f"{BASE_URL}/books", json={"title": book_title})
        if response.status_code == 201:
            return response.json().get("message", "✅ Book added successfully!")
        return f"❌ Error: {response.json().get('error', 'Unexpected error')}"
    except requests.exceptions.RequestException as e:
        return f"❌ Error: Failed to connect to the API - {str(e)}"

# Add a review to a book
def add_book_review(book_id, rating, note):
    if not book_id.isdigit():
        return "❌ Error: Book ID must be an integer!"
    if not (0 <= float(rating) <= 5):
        return "❌ Error: Rating must be between 0 and 5!"
    if not note.strip():
        return "❌ Error: Review note cannot be empty!"
    try:
        response = requests.post(
            f"{BASE_URL}/books/{book_id}/reviews",
            json={"rating": float(rating), "note": note},
        )
        if response.status_code == 201:
            return response.json().get("message", "✅ Review added successfully!")
        return f"❌ Error: {response.json().get('error', 'Unexpected error')}"
    except requests.exceptions.RequestException as e:
        return f"❌ Error: Failed to connect to the API - {str(e)}"

# View all books and their reviews
def view_books():
    try:
        response = requests.get(f"{BASE_URL}/books")
        if response.status_code == 200:
            books = response.json()
            if not books:
                return "📚 Your book list is empty. Add some books to get started!"
            output = ["📚 Book List:"]
            for book in books:
                output.append(f"Book #{book['id']}: {book['title']}")
                if not book["reviews"]:
                    output.append("   No reviews yet.")
                else:
                    for review in book["reviews"]:
                        output.append(
                            f"   Review #{review['review_id']} | Rating: {review['rating']}/5 | {review['note']}"
                        )
            return "\n".join(output)
        return f"❌ Error: {response.json().get('error', 'Unexpected error')}"
    except requests.exceptions.RequestException as e:
        return f"❌ Error: Failed to connect to the API - {str(e)}"

# Delete a book
def delete_book(book_id):
    if not book_id.isdigit():
        return "❌ Error: Book ID must be an integer!"
    try:
        response = requests.delete(f"{BASE_URL}/books/{book_id}")
        if response.status_code == 200:
            return response.json().get("message", "✅ Book deleted successfully!")
        return f"❌ Error: {response.json().get('error', 'Unexpected error')}"
    except requests.exceptions.RequestException as e:
        return f"❌ Error: Failed to connect to the API - {str(e)}"

# Delete a review for a book
def delete_book_review(book_id, review_id):
    if not book_id.isdigit() or not review_id.isdigit():
        return "❌ Error: Both Book ID and Review ID must be integers!"
    try:
        response = requests.delete(f"{BASE_URL}/books/{book_id}/reviews/{review_id}")
        if response.status_code == 200:
            return response.json().get("message", "✅ Review deleted successfully!")
        return f"❌ Error: {response.json().get('error', 'Unexpected error')}"
    except requests.exceptions.RequestException as e:
        return f"❌ Error: Failed to connect to the API - {str(e)}"

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("# 🎥 Movie & 📚 Book Manager with Reviews")
    
    with gr.Tab("Movies"):
        with gr.Row():
            gr.Markdown("## Add a Movie")
            movie_input = gr.Textbox(label="Movie Name", placeholder="Enter movie name...")
            movie_add_btn = gr.Button("Add Movie")
            movie_output = gr.Textbox(label="Status")
            movie_add_btn.click(add_movie_frontend, inputs=movie_input, outputs=movie_output)
        
        with gr.Row():
            gr.Markdown("## Add a Review")
            movie_id_input = gr.Textbox(label="Movie ID", placeholder="Enter movie ID...")
            rating_input = gr.Slider(0, 5, step=0.5, label="Rating")
            review_input = gr.Textbox(label="Review Note", placeholder="Write your review...")
            review_add_btn = gr.Button("Add Review")
            review_output = gr.Textbox(label="Status")
            review_add_btn.click(add_movie_review, inputs=[movie_id_input, rating_input, review_input], outputs=review_output)
        
        with gr.Row():
            gr.Markdown("## View Movies")
            view_movies_btn = gr.Button("View All Movies")
            movies_display = gr.Textbox(label="Movie List", interactive=False)
            view_movies_btn.click(view_movies, inputs=[], outputs=movies_display)

        with gr.Row():
            del_book_input = gr.Textbox(label="Delete Movie ID", placeholder="Enter movie ID...")
            del_book_btn = gr.Button("Delete movie")
            del_book_output = gr.Textbox(label="Status")
            del_book_btn.click(delete_book, inputs=del_book_input, outputs=del_book_output)

        with gr.Row():
            del_movie_id_input = gr.Textbox(label="Movie ID", placeholder="Enter MOvie ID...")
            del_review_id_input = gr.Textbox(label="Review ID", placeholder="Enter review ID...")
            del_review_btn = gr.Button("Delete Review")
            del_review_output = gr.Textbox(label="Status")
            del_review_btn.click(
                delete_movie_review,
                inputs=[del_movie_id_input, del_review_id_input],
                outputs=del_review_output,
            )

    
    with gr.Tab("Books"):
        with gr.Row():
            gr.Markdown("## Add a Book")
            book_input = gr.Textbox(label="Book Title", placeholder="Enter book title...")
            book_add_btn = gr.Button("Add Book")
            book_output = gr.Textbox(label="Status")
            book_add_btn.click(add_book_frontend, inputs=book_input, outputs=book_output)
          
        with gr.Row():
            book_id_input = gr.Textbox(label="Book ID", placeholder="Enter book ID...")
            rating_input = gr.Slider(0, 5, step=0.5, label="Rating")
            review_input = gr.Textbox(label="Review Note", placeholder="Write your review...")
            review_add_btn = gr.Button("Add Review")
            review_output = gr.Textbox(label="Status")
            review_add_btn.click(
                add_book_review,
                inputs=[book_id_input, rating_input, review_input],
                outputs=review_output,
            )
        
        with gr.Row():
            gr.Markdown("## View Books")
            view_books_btn = gr.Button("View All Books")
            books_display = gr.Textbox(label="Book List", interactive=False)
            view_books_btn.click(view_books, inputs=[], outputs=books_display)
    
        with gr.Row():
            del_book_input = gr.Textbox(label="Delete Book ID", placeholder="Enter book ID...")
            del_book_btn = gr.Button("Delete Book")
            del_book_output = gr.Textbox(label="Status")
            del_book_btn.click(delete_book, inputs=del_book_input, outputs=del_book_output)

       
        with gr.Row():
            del_book_id_input = gr.Textbox(label="Book ID", placeholder="Enter book ID...")
            del_review_id_input = gr.Textbox(label="Review ID", placeholder="Enter review ID...")
            del_review_btn = gr.Button("Delete Review")
            del_review_output = gr.Textbox(label="Status")
            del_review_btn.click(
                delete_book_review,
                inputs=[del_book_id_input, del_review_id_input],
                outputs=del_review_output,
            )

# Launch Gradio App
if __name__ == "__main__":
    demo.launch()
