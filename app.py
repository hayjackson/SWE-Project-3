import gradio as gr
import requests

# Base URL of the Flask API
BASE_URL = "http://127.0.0.1:5000"
 
# Functions to interact with the API


# First: Movie Tab functions, Aditi, Dec 2

# Adding a movie
def add_movie_frontend(movie_name, genre):
    # Aditi, dec 2, 2024
    if not movie_name.strip():
        return "❌ Error: Movie name cannot be empty!"
    if not genre.strip():
        return "❌ Error: Genre cannot be empty!"
    try:
        response = requests.post(f"{BASE_URL}/movies", json={"name": movie_name, "genre": genre})
        if response.status_code == 201:
            return response.json().get("message", "✅ Movie added successfully!")
        return f"❌ Error: {response.json().get('error', 'Unexpected error')}"
    except requests.exceptions.RequestException as e:
        return f"❌ Error: Failed to connect to the API - {str(e)}"

# Adding a review to a movie
def add_review_frontend(movie_id, rating, note):
    # Aditi, Dec 2, 2024
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

# Editing a review
def edit_review_frontend(movie_id, review_id, rating, note):
    # Aditi, Dec 2, 2024
    if not movie_id.isdigit() or not review_id.isdigit():
        return "❌ Error: Both Movie ID and Review ID must be integers!"
    try:
        response = requests.put(
            f"{BASE_URL}/movies/{movie_id}/reviews/{review_id}",
            json={"rating": float(rating), "note": note},
        )
        return response.json().get("message", "✅ Review updated successfully!")
    except requests.exceptions.RequestException as e:
        return f"❌ Error: Failed to connect to the API - {str(e)}"

# Deleting a review
def delete_review_frontend(movie_id, review_id):
    # Aditi, Dec 2, 2024
    if not movie_id.isdigit() or not review_id.isdigit():
        return "❌ Error: Both Movie ID and Review ID must be integers!"
    try:
        response = requests.delete(f"{BASE_URL}/movies/{movie_id}/reviews/{review_id}")
        return response.json().get("message", "✅ Review deleted successfully!")
    except requests.exceptions.RequestException as e:
        return f"❌ Error: Failed to connect to the API - {str(e)}"

# Deleting a movie
def delete_movie_frontend(movie_id):
    # Aditi, Dec 2, 2024
    if not movie_id.isdigit():
        return "❌ Error: Movie ID must be an integer!"
    try:
        response = requests.delete(f"{BASE_URL}/movies/{movie_id}")
        return response.json().get("message", "✅ Movie deleted successfully!")
    except requests.exceptions.RequestException as e:
        return f"❌ Error: Failed to connect to the API - {str(e)}"


# Searching by genre
def search_by_genre_frontend(genre):
    # Aditi, Dec 2, 2024
    if not genre.strip():
        return "❌ Error: Genre cannot be empty!"
    try:
        response = requests.get(f"{BASE_URL}/movies/genre", params={"genre": genre})
        if response.status_code == 200:
            movies = response.json()
            if not movies:
                return f"🎥 No movies found under genre '{genre}'."
            output = [f"🎥 Movies under genre '{genre}':"]
            for movie in movies:
                output.append(f"Movie #{movie['id']}: {movie['name']}")
            return "\n".join(output)
        return f"❌ Error: {response.json().get('error', 'Unexpected error')}"
    except requests.exceptions.RequestException as e:
        return f"❌ Error: Failed to connect to the API - {str(e)}"


# Viewing all movies
def view_movies_frontend():
    # Aditi, Dec 2, 2024
    try:
        response = requests.get(f"{BASE_URL}/movies")
        if response.status_code == 200:
            movies = response.json()
            if not movies:
                return "🎥 No movies found. Add some to get started!"
            output = ["🎥 Movie List:"]
            for movie in movies:
                output.append(f"Movie #{movie['id']}: {movie['name']} (Genre: {movie['genre']})")
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

# Searching reviews by movie ID
def search_reviews_frontend(movie_id):
    # Aditi, Dec 2, 2024
    if not movie_id.isdigit():
        return "❌ Error: Movie ID must be an integer!"
    try:
        response = requests.get(f"{BASE_URL}/movies/{movie_id}/reviews")
        if response.status_code == 200:
            movie = response.json()
            output = [f"🎥 Movie: {movie['name']} (Genre: {movie['genre']})"]
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

# def delete_book_review(book_id, review_id):
#     response = requests.delete(f"{API_BASE_URL}/books/{book_id}")
#     if response.status_code == 200:
#         return response.json()["message"]
#     return response.json()["error"]



# tv_show 

def add_show_frontend(title, genre, rating):
    try:
        response = requests.post(f"{BASE_URL}/tv_shows", json={"title": title, "genre": genre, "rating": rating})
        response.raise_for_status()  
        if response.status_code == 200:
            return "TV Show added successfully"
        else:
            return f"Error: {response.json().get('error', 'Unknown error occurred')}"
    except requests.RequestException as e:
        return f"Error: Failed to connect to the API - {str(e)}"
def edit_show_frontend(show_id, title, genre, rating):
    # Edited, Dec 4, 2024
    if not show_id.isdigit():
        return "Error: Show ID must be an integer!"
    if not title.strip():
        return "Error: Title cannot be empty!"
    if not genre.strip():
        return "Error: Genre cannot be empty!"
    if not (0 <= float(rating) <= 5):
        return "Error: Rating must be between 0 and 5!"
    try:
        response = requests.put(
            f"{BASE_URL}/tv_shows/{show_id}",
            json={"title": title, "genre": genre, "rating": rating},
        )
        if response.status_code == 200:
            return response.json().get("message", "TV Show updated successfully!")
        return f"Error: {response.json().get('error', 'Unexpected error')}"
    except requests.exceptions.RequestException as e:
        return f"Error: Failed to connect to the API - {str(e)}"


def delete_show_frontend(show_id):
    # Edited, Dec 4, 2024
    if not show_id.isdigit():
        return "Error: Show ID must be an integer!"
    try:
        response = requests.delete(f"{BASE_URL}/tv_shows/{show_id}")
        if response.status_code == 200:
            return response.json().get("message", "TV Show deleted successfully!")
        return f"Error: {response.json().get('error', 'Unexpected error')}"
    except requests.exceptions.RequestException as e:
        return f"Error: Failed to connect to the API - {str(e)}"


def search_shows_frontend(query):
    # Edited, Dec 4, 2024
    if not query.strip():
        return "Error: Search query cannot be empty!"
    try:
        response = requests.get(f"{BASE_URL}/tv_shows/search", params={"query": query})
        if response.status_code == 200:
            shows = response.json()
            if not shows:
                return "No shows found matching the search query."
            output = ["Search Results:"]
            for show in shows:
                output.append(
                    f"ID: {show['id']}, Title: {show['title']}, Genre: {show['genre']}, Rating: {show['rating']}"
                )
            return "\n".join(output)
        return f"Error: {response.json().get('error', 'Unexpected error')}"
    except requests.exceptions.RequestException as e:
        return f"Error: Failed to connect to the API - {str(e)}"


def filter_shows_by_genre_frontend(genre):
    # Edited, Dec 4, 2024
    if not genre.strip():
        return "Error: Genre cannot be empty!"
    try:
        response = requests.get(f"{BASE_URL}/tv_shows/genre", params={"genre": genre})
        if response.status_code == 200:
            shows = response.json()
            if not shows:
                return f"No shows found under genre '{genre}'."
            output = [f"Shows under genre '{genre}':"]
            for show in shows:
                output.append(
                    f"ID: {show['id']}, Title: {show['title']}, Genre: {show['genre']}, Rating: {show['rating']}"
                )
            return "\n".join(output)
        return f"Error: {response.json().get('error', 'Unexpected error')}"
    except requests.exceptions.RequestException as e:
        return f"Error: Failed to connect to the API - {str(e)}"


def view_shows_frontend():
    # Edited, Dec 4, 2024
    try:
        response = requests.get(f"{BASE_URL}/tv_shows")
        if response.status_code == 200:
            shows = response.json()
            if not shows:
                return "No TV shows found. Add some to get started!"
            output = ["TV Shows List:"]
            for show in shows:
                output.append(
                    f"ID: {show['id']}, Title: {show['title']}, Genre: {show['genre']}, Rating: {show['rating']}"
                )
            return "\n".join(output)
        return f"Error: {response.json().get('error', 'Unexpected error')}"
    except requests.exceptions.RequestException as e:
        return f"Error: Failed to connect to the API - {str(e)}"


# Gradio Interface

# First: Movies tab:
with gr.Blocks() as demo:
    gr.Markdown("# 🎥 Movie Review App")
    
    with gr.Tab("Home Page"):
       
       
        with gr.Row():
            gr.Markdown("# Welcome to our Media Recommendation App!!")
            #Display Genres
            movie_genres = gr.Textbox(label = "Movies genres", min_width= 20, text_align='left')
        # Display Top Movies
        with gr.Row():
            top_movies = gr.Textbox(label = "Top rated movies", elem_id= 'custom-textbox')


    with gr.Tab("Add a Movie"):
        movie_name_input = gr.Textbox(label="Movie Name", placeholder="Enter movie name...")
        genre_input = gr.Textbox(label="Genre", placeholder="Enter movie genre...")
        movie_add_btn = gr.Button("Add Movie")
        movie_output = gr.Textbox(label="Status")
        movie_add_btn.click(add_movie_frontend, inputs=[movie_name_input, genre_input], outputs=movie_output)

    with gr.Tab("Add a Review"):
        movie_id_input = gr.Textbox(label="Movie ID", placeholder="Enter movie ID...")
        rating_input = gr.Slider(0, 5, step=0.5, label="Rating")
        review_note_input = gr.Textbox(label="Review Note", placeholder="Write your review...")
        review_add_btn = gr.Button("Add Review")
        review_output = gr.Textbox(label="Status")
        review_add_btn.click(
            add_review_frontend,
            inputs=[movie_id_input, rating_input, review_note_input],
            outputs=review_output,
        )

    with gr.Tab("Edit a Review"):
        edit_movie_id_input = gr.Textbox(label="Movie ID", placeholder="Enter movie ID...")
        edit_review_id_input = gr.Textbox(label="Review ID", placeholder="Enter review ID...")
        edit_rating_input = gr.Slider(0, 5, step=0.5, label="New Rating")
        edit_review_note_input = gr.Textbox(label="New Review Note", placeholder="Update your review...")
        edit_review_btn = gr.Button("Edit Review")
        edit_review_output = gr.Textbox(label="Status")
        edit_review_btn.click(
            edit_review_frontend,
            inputs=[edit_movie_id_input, edit_review_id_input, edit_rating_input, edit_review_note_input],
            outputs=edit_review_output,
        )

    with gr.Tab("Delete a Movie"):
        del_movie_input = gr.Textbox(label="Delete Movie ID", placeholder="Enter movie ID...")
        del_movie_btn = gr.Button("Delete Movie")
        del_movie_output = gr.Textbox(label="Status")
        del_movie_btn.click(delete_movie_frontend, inputs=del_movie_input, outputs=del_movie_output)

    with gr.Tab("Delete a Review"):
        del_movie_id_input = gr.Textbox(label="Movie ID", placeholder="Enter movie ID...")
        del_review_id_input = gr.Textbox(label="Review ID", placeholder="Enter review ID...")
        del_review_btn = gr.Button("Delete Review")
        del_review_output = gr.Textbox(label="Status")
        del_review_btn.click(
            delete_review_frontend,
            inputs=[del_movie_id_input, del_review_id_input],
            outputs=del_review_output,
        )

    with gr.Tab("Search by Genre"):
        genre_search_input = gr.Textbox(label="Genre", placeholder="Enter genre to search...")
        genre_search_btn = gr.Button("Search by Genre")
        genre_search_output = gr.Textbox(label="Movies by Genre", interactive=False)
        genre_search_btn.click(search_by_genre_frontend, inputs=genre_search_input, outputs=genre_search_output)

    with gr.Tab("Search Reviews by Movie ID"):
        search_movie_id_input = gr.Textbox(label="Movie ID", placeholder="Enter movie ID...")
        search_reviews_btn = gr.Button("Search Reviews")
        search_reviews_output = gr.Textbox(label="Reviews", interactive=False)
        search_reviews_btn.click(search_reviews_frontend, inputs=search_movie_id_input, outputs=search_reviews_output)

    with gr.Tab("View Movies"):
        view_movies_btn = gr.Button("View All Movies")
        movies_display = gr.Textbox(label="Movie List", interactive=False)
        view_movies_btn.click(view_movies_frontend, inputs=[], outputs=movies_display)



        

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




        
#tv_show
    with gr.Tab("TV Shows"):
        gr.Markdown("## 📺 TV Show Reviews")

        with gr.Tab("Add a TV Show"):
            show_title_input = gr.Textbox(label="TV Show Title", placeholder="Enter TV show title...")
            show_genre_input = gr.Textbox(label="Genre", placeholder="Enter TV show genre...")
            show_rating_input = gr.Slider(0, 10, step=0.1, label="Rating")
            show_add_btn = gr.Button("Add TV Show")
            show_output = gr.Textbox(label="Status")
            show_add_btn.click(add_show_frontend, inputs=[show_title_input, show_genre_input, show_rating_input], outputs=show_output)

        with gr.Tab("Edit a TV Show"):
            edit_show_id_input = gr.Textbox(label="TV Show ID", placeholder="Enter TV show ID...")
            edit_show_title_input = gr.Textbox(label="New Title", placeholder="Enter new title...")
            edit_show_genre_input = gr.Textbox(label="New Genre", placeholder="Enter new genre...")
            edit_show_rating_input = gr.Slider(0, 10, step=0.1, label="New Rating")
            edit_show_btn = gr.Button("Edit TV Show")
            edit_show_output = gr.Textbox(label="Status")
            edit_show_btn.click(
                edit_show_frontend,
                inputs=[edit_show_id_input, edit_show_title_input, edit_show_genre_input, edit_show_rating_input],
                outputs=edit_show_output,
            )

        with gr.Tab("Delete a TV Show"):
            del_show_input = gr.Textbox(label="Delete TV Show ID", placeholder="Enter TV show ID...")
            del_show_btn = gr.Button("Delete TV Show")
            del_show_output = gr.Textbox(label="Status")
            del_show_btn.click(delete_show_frontend, inputs=del_show_input, outputs=del_show_output)

        with gr.Tab("Search TV Shows"):
            show_search_input = gr.Textbox(label="Search Query", placeholder="Enter search term...")
            show_search_btn = gr.Button("Search TV Shows")
            show_search_output = gr.Textbox(label="Search Results", interactive=False)
            show_search_btn.click(search_shows_frontend, inputs=show_search_input, outputs=show_search_output)

        with gr.Tab("Filter TV Shows by Genre"):
            show_genre_filter_input = gr.Textbox(label="Genre", placeholder="Enter genre to filter...")
            show_genre_filter_btn = gr.Button("Filter by Genre")
            show_genre_filter_output = gr.Textbox(label="Filtered TV Shows", interactive=False)
            show_genre_filter_btn.click(filter_shows_by_genre_frontend, inputs=show_genre_filter_input, outputs=show_genre_filter_output)

        with gr.Tab("View All TV Shows"):
            view_shows_btn = gr.Button("View All TV Shows")
            shows_display = gr.Textbox(label="TV Show List", interactive=False)
            view_shows_btn.click(view_shows_frontend, inputs=[], outputs=shows_display)
            
if __name__ == "__main__":
    
    demo.launch()
