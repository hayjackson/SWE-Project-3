# Frontend of the Movies Tab
# Rebecca Rogovich

import gradio as gr
import json
import os

DATABASE_FILE = 'movie_reviews.json'

# Load and save functions
def load_data():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'r') as file:
            return json.load(file)
    return {"movies": []}

def save_data(data):
    with open(DATABASE_FILE, 'w') as file:
        json.dump(data, file, indent=4)


# Core functions
def add_movie_interface(movie_name):
    if not movie_name.strip():
        return "❌ Error: Movie name cannot be empty!"
    try:
        data = load_data()
        movie = {
            "id": len(data["movies"]) + 1,
            "name": movie_name,
            "reviews": []
        }
        data["movies"].append(movie)
        save_data(data)
        return f"✅ Success: '{movie_name}' added to your collection!"
    except Exception as e:
        return f"❌ Error: Failed to add movie - {str(e)}"

def add_review_interface(movie_id, rating, review_text):
    try:
        movie_id = int(movie_id)
        rating = float(rating)
        if not (0 <= rating <= 5):
            return "❌ Error: Rating must be between 0 and 5!"
        
        data = load_data()
        for movie in data["movies"]:
            if movie["id"] == movie_id:
                review_id = len(movie["reviews"]) + 1
                review = {
                    "review_id": review_id,
                    "rating": rating,
                    "note": review_text
                }
                movie["reviews"].append(review)
                save_data(data)
                return f"✅ Review successfully added to '{movie['name']}'"
        return f"❌ Error: Movie with ID {movie_id} not found!"
    except ValueError:
        return "❌ Error: Invalid movie ID or rating format!"
    except Exception as e:
        return f"❌ Error: Failed to add review - {str(e)}"

def view_all_movies_reviews():
    try:
        data = load_data()
        if not data["movies"]:
            return "🎥 Your movie collection is empty. Add some movies to get started!"
        
        output = []
        output.append("╔══════════════════════════════════════╗")
        output.append("║        🎥 YOUR MOVIE COLLECTION 🎥    ║")
        output.append("╚══════════════════════════════════════╝\n")
        
        for movie in data["movies"]:
            output.append(f"🎬 Movie #{movie['id']} | {movie['name']}")
            if not movie["reviews"]:
                output.append("   💭 No reviews yet")
            else:
                for review in movie["reviews"]:
                    stars = "⭐" * int(review['rating'])
                    half_star = "✨" if review['rating'] % 1 >= 0.5 else ""
                    output.append(f"\n   Review #{review['review_id']}")
                    output.append(f"   Rating: {stars}{half_star} ({review['rating']}/5)")
                    output.append(f"   📝 {review['note']}")
            output.append("\n" + "─" * 50 + "\n")
        
        return "\n".join(output)
    except Exception as e:
        return f"❌ Error: Failed to load reviews - {str(e)}"

def delete_movie_interface(movie_id):
    try:
        movie_id = int(movie_id)
        data = load_data()
        initial_length = len(data["movies"])
        data["movies"] = [movie for movie in data["movies"] if movie["id"] != movie_id]
        if len(data["movies"]) == initial_length:
            return f"❌ Error: Movie #{movie_id} not found!"
        save_data(data)
        return f"✅ Movie #{movie_id} and its reviews have been removed."
    except ValueError:
        return "❌ Error: Invalid movie ID format!"
    except Exception as e:
        return f"❌ Error: Failed to delete movie - {str(e)}"

def delete_review_interface(movie_id, review_id):
    try:
        movie_id = int(movie_id)
        review_id = int(review_id)
        data = load_data()
        for movie in data["movies"]:
            if movie["id"] == movie_id:
                initial_length = len(movie["reviews"])
                movie["reviews"] = [r for r in movie["reviews"] if r["review_id"] != review_id]
                if len(movie["reviews"]) == initial_length:
                    return f"❌ Error: Review #{review_id} not found!"
                save_data(data)
                return f"✅ Review #{review_id} removed from '{movie['name']}'"
        return f"❌ Error: Movie #{movie_id} not found!"
    except ValueError:
        return "❌ Error: Invalid movie ID or review ID format!"
    except Exception as e:
        return f"❌ Error: Failed to delete review - {str(e)}"


# Gradio interface
with gr.Blocks(
    title="Movie Review Manager",
    theme=gr.themes.Soft(
        primary_hue="green",
        secondary_hue="blue",
        neutral_hue="slate",
        font=gr.themes.GoogleFont("Roboto")
    )
) as demo:
    gr.Markdown(
        """
        # 🎥 Movie Review Manager
        Keep track of your favorite movies and share your reviews!
        
        ---
        """
    )
    
    with gr.Tab("🎬 Add Movie"):
        gr.Markdown("### Add a New Movie to Your Collection")
        with gr.Row():
            movie_input = gr.Textbox(
                label="Movie Title",
                placeholder="Enter the title of the movie...",
                scale=3
            )
            add_movie_btn = gr.Button("🎬 Add Movie", scale=1, variant="primary")
        add_movie_output = gr.Textbox(label="Status", interactive=False)
        add_movie_btn.click(add_movie_interface, inputs=[movie_input], outputs=[add_movie_output])
    
    with gr.Tab("⭐ Add Review"):
        gr.Markdown("### Share Your Thoughts")
        with gr.Row():
            movie_id_input = gr.Textbox(
                label="Movie ID",
                placeholder="Enter the movie's ID number...",
                scale=1
            )
            rating_input = gr.Slider(
                minimum=0,
                maximum=5,
                step=0.5,
                label="Rating",
                value=5,
                scale=2
            )
        review_input = gr.Textbox(
            label="Your Review",
            placeholder="Share your thoughts about the movie...",
            lines=3
        )
        add_review_btn = gr.Button("⭐ Add Review", variant="primary")
        add_review_output = gr.Textbox(label="Status", interactive=False)
        add_review_btn.click(
            add_review_interface, 
            inputs=[movie_id_input, rating_input, review_input],
            outputs=[add_review_output]
        )
    
    with gr.Tab("🎥 View Collection"):
        with gr.Row():
            view_all_btn = gr.Button("🎬 View All Movies", scale=2, variant="primary")
            refresh_btn = gr.Button("🔄 Refresh", scale=1)
        view_output = gr.Textbox(
            label="Your Movie Collection",
            interactive=False,
            lines=15,
            show_copy_button=True
        )
        view_all_btn.click(view_all_movies_reviews, inputs=[], outputs=[view_output])
        refresh_btn.click(view_all_movies_reviews, inputs=[], outputs=[view_output])
    
    with gr.Tab("🗑️ Manage"):
        with gr.Row():
            gr.Markdown(
                """
                ### Remove Movie
                Delete a movie and all its reviews from your collection
                """
            )
        with gr.Row():
            del_movie_input = gr.Textbox(
                label="Movie ID",
                placeholder="Enter the movie's ID number...",
                scale=3
            )
            del_movie_btn = gr.Button("🗑️ Delete Movie", scale=1, variant="secondary")
        del_movie_output = gr.Textbox(label="Status", interactive=False)
        del_movie_btn.click(delete_movie_interface, inputs=[del_movie_input], outputs=[del_movie_output])
        
        gr.Markdown("---")
        
        with gr.Row():
            gr.Markdown(
                """
                ### Remove Review
                Delete a specific review from a movie
                """
            )
        with gr.Row():
            del_review_movie_input = gr.Textbox(
                label="Movie ID",
                placeholder="Enter the movie's ID number...",
                scale=2
            )
            del_review_input = gr.Textbox(
                label="Review ID",
                placeholder="Enter the review's ID number...",
                scale=2
            )
        del_review_btn = gr.Button("🗑️ Delete Review", variant="secondary")
        del_review_output = gr.Textbox(label="Status", interactive=False)
        del_review_btn.click(
            delete_review_interface, 
            inputs=[del_review_movie_input, del_review_input],
            outputs=[del_review_output]
        )

if __name__ == "__main__":

