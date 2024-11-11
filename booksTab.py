import gradio as gr
import json
import os


# Using the same database file as the backend
DATABASE_FILE = 'book_reviews.json'

# Loading and saving functions remain the same
def load_data():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'r') as file:
            return json.load(file)
    return {"books": []}

def save_data(data):
    with open(DATABASE_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Core functions remain the same
def add_book_interface(book_title):
    if not book_title.strip():
        return "❌ Error: Book title cannot be empty!"
    try:
        data = load_data()
        book = {
            "id": len(data["books"]) + 1,
            "title": book_title,
            "reviews": []
        }
        data["books"].append(book)
        save_data(data)
        return f"✅ Success: '{book_title}' added to your library!"
    except Exception as e:
        return f"❌ Error: Failed to add book - {str(e)}"

def add_review_interface(book_id, rating, review_text):
    try:
        book_id = int(book_id)
        rating = float(rating)
        if not (0 <= rating <= 5):
            return "❌ Error: Rating must be between 0 and 5!"
        
        data = load_data()
        for book in data["books"]:
            if book["id"] == book_id:
                review_id = len(book["reviews"]) + 1
                review = {
                    "review_id": review_id,
                    "rating": rating,
                    "note": review_text
                }
                book["reviews"].append(review)
                save_data(data)
                return f"✅ Review successfully added to '{book['title']}'"
        return f"❌ Error: Book with ID {book_id} not found!"
    except ValueError:
        return "❌ Error: Invalid book ID or rating format!"
    except Exception as e:
        return f"❌ Error: Failed to add review - {str(e)}"

def view_all_books_reviews():
    try:
        data = load_data()
        if not data["books"]:
            return "📚 Your library is empty. Add some books to get started!"
        
        output = []
        output.append("╔══════════════════════════════════════╗")
        output.append("║         📚 YOUR BOOK LIBRARY 📚      ║")
        output.append("╚══════════════════════════════════════╝\n")
        
        for book in data["books"]:
            output.append(f"📖 Book #{book['id']} | {book['title']}")
            if not book["reviews"]:
                output.append("   💭 No reviews yet")
            else:
                for review in book["reviews"]:
                    stars = "⭐" * int(review['rating'])
                    half_star = "✨" if review['rating'] % 1 >= 0.5 else ""
                    output.append(f"\n   Review #{review['review_id']}")
                    output.append(f"   Rating: {stars}{half_star} ({review['rating']}/5)")
                    output.append(f"   📝 {review['note']}")
            output.append("\n" + "─" * 50 + "\n")
        
        return "\n".join(output)
    except Exception as e:
        return f"❌ Error: Failed to load reviews - {str(e)}"

def delete_book_interface(book_id):
    try:
        book_id = int(book_id)
        data = load_data()
        initial_length = len(data["books"])
        data["books"] = [book for book in data["books"] if book["id"] != book_id]
        if len(data["books"]) == initial_length:
            return f"❌ Error: Book #{book_id} not found!"
        save_data(data)
        return f"✅ Book #{book_id} and its reviews have been removed."
    except ValueError:
        return "❌ Error: Invalid book ID format!"
    except Exception as e:
        return f"❌ Error: Failed to delete book - {str(e)}"

def delete_review_interface(book_id, review_id):
    try:
        book_id = int(book_id)
        review_id = int(review_id)
        data = load_data()
        for book in data["books"]:
            if book["id"] == book_id:
                initial_length = len(book["reviews"])
                book["reviews"] = [r for r in book["reviews"] if r["review_id"] != review_id]
                if len(book["reviews"]) == initial_length:
                    return f"❌ Error: Review #{review_id} not found!"
                save_data(data)
                return f"✅ Review #{review_id} removed from '{book['title']}'"
        return f"❌ Error: Book #{book_id} not found!"
    except ValueError:
        return "❌ Error: Invalid book ID or review ID format!"
    except Exception as e:
        return f"❌ Error: Failed to delete review - {str(e)}"

# Create the enhanced Gradio interface
with gr.Blocks(
    title="Book Review Manager",
    theme=gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="indigo",
        neutral_hue="slate",
        font=gr.themes.GoogleFont("Poppins")
    )
) as demo:
    gr.Markdown(
        """
        # 📚 Book Review Manager
        Keep track of your reading journey and share your thoughts on your favorite books!
        
        ---
        """
    )
    
    with gr.Tab("📖 Add Book"):
        gr.Markdown("### Add a New Book to Your Library")
        with gr.Row():
            book_input = gr.Textbox(
                label="Book Title",
                placeholder="Enter the title of the book...",
                scale=3
            )
            add_book_btn = gr.Button("📚 Add Book", scale=1, variant="primary")
        add_book_output = gr.Textbox(label="Status", interactive=False)
        add_book_btn.click(add_book_interface, inputs=[book_input], outputs=[add_book_output])
    
    with gr.Tab("⭐ Add Review"):
        gr.Markdown("### Share Your Thoughts")
        with gr.Row():
            book_id_input = gr.Textbox(
                label="Book ID",
                placeholder="Enter the book's ID number...",
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
            placeholder="Share your thoughts about the book...",
            lines=3
        )
        add_review_btn = gr.Button("⭐ Add Review", variant="primary")
        add_review_output = gr.Textbox(label="Status", interactive=False)
        add_review_btn.click(
            add_review_interface, 
            inputs=[book_id_input, rating_input, review_input],
            outputs=[add_review_output]
        )
    
    with gr.Tab("📚 View Library"):
        with gr.Row():
            view_all_btn = gr.Button("📖 View All Books", scale=2, variant="primary")
            refresh_btn = gr.Button("🔄 Refresh", scale=1)
        view_output = gr.Textbox(
            label="Your Book Library",
            interactive=False,
            lines=15,
            show_copy_button=True
        )
        view_all_btn.click(view_all_books_reviews, inputs=[], outputs=[view_output])
        refresh_btn.click(view_all_books_reviews, inputs=[], outputs=[view_output])
    
    with gr.Tab("🗑️ Manage"):
        with gr.Row():
            gr.Markdown(
                """
                ### Remove Book
                Delete a book and all its reviews from your library
                """
            )
        with gr.Row():
            del_book_input = gr.Textbox(
                label="Book ID",
                placeholder="Enter the book's ID number...",
                scale=3
            )
            del_book_btn = gr.Button("🗑️ Delete Book", scale=1, variant="secondary")
        del_book_output = gr.Textbox(label="Status", interactive=False)
        del_book_btn.click(delete_book_interface, inputs=[del_book_input], outputs=[del_book_output])
        
        gr.Markdown("---")
        
        with gr.Row():
            gr.Markdown(
                """
                ### Remove Review
                Delete a specific review from a book
                """
            )
        with gr.Row():
            del_review_book_input = gr.Textbox(
                label="Book ID",
                placeholder="Enter the book's ID number...",
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
            inputs=[del_review_book_input, del_review_input],
            outputs=[del_review_output]
        )

if __name__ == "__main__":
    demo.launch()