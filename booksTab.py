import gradio as gr
import json
import os

# Using the same database file as the backend
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

def add_book_interface(book_title):
    if not book_title.strip():
        return "Error: Book title cannot be empty!"
    try:
        data = load_data()
        book = {
            "id": len(data["books"]) + 1,
            "title": book_title,
            "reviews": []
        }
        data["books"].append(book)
        save_data(data)
        return f"Success: Book '{book_title}' added successfully!"
    except Exception as e:
        return f"Error: Failed to add book - {str(e)}"

def add_review_interface(book_id, rating, review_text):
    try:
        book_id = int(book_id)
        rating = float(rating)
        if not (0 <= rating <= 5):
            return "Error: Rating must be between 0 and 5!"
        
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
                return f"Success: Review added to book '{book['title']}'"
        return f"Error: Book with ID {book_id} not found!"
    except ValueError:
        return "Error: Invalid book ID or rating format!"
    except Exception as e:
        return f"Error: Failed to add review - {str(e)}"

def view_all_books_reviews():
    try:
        data = load_data()
        if not data["books"]:
            return "No books or reviews found."
        
        output = []
        output.append("📚 BOOKS AND REVIEWS 📚\n")
        for book in data["books"]:
            output.append(f"\nBOOK ID: {book['id']} | TITLE: {book['title']}")
            if not book["reviews"]:
                output.append("   No reviews yet")
            else:
                for review in book["reviews"]:
                    stars = "⭐" * int(review['rating'])
                    output.append(f"\n   Review #{review['review_id']}")
                    output.append(f"   Rating: {stars} ({review['rating']}/5)")
                    output.append(f"   Note: {review['note']}")
            output.append("\n" + "-"*50)
        
        return "\n".join(output)
    except Exception as e:
        return f"Error: Failed to load reviews - {str(e)}"

def delete_book_interface(book_id):
    try:
        book_id = int(book_id)
        data = load_data()
        initial_length = len(data["books"])
        data["books"] = [book for book in data["books"] if book["id"] != book_id]
        if len(data["books"]) == initial_length:
            return f"Error: Book with ID {book_id} not found!"
        save_data(data)
        return f"Success: Book ID {book_id} and its reviews have been deleted."
    except ValueError:
        return "Error: Invalid book ID format!"
    except Exception as e:
        return f"Error: Failed to delete book - {str(e)}"

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
                    return f"Error: Review ID {review_id} not found!"
                save_data(data)
                return f"Success: Review {review_id} deleted from '{book['title']}'"
        return f"Error: Book with ID {book_id} not found!"
    except ValueError:
        return "Error: Invalid book ID or review ID format!"
    except Exception as e:
        return f"Error: Failed to delete review - {str(e)}"

# Create the Gradio interface
with gr.Blocks(title="Book Review Manager") as demo:
    gr.Markdown("# 📚 Book Review Management System")
    
    with gr.Tab("Add Book"):
        with gr.Row():
            book_input = gr.Textbox(label="Book Title")
            add_book_btn = gr.Button("Add Book")
        add_book_output = gr.Textbox(label="Result", interactive=False)
        add_book_btn.click(add_book_interface, inputs=[book_input], outputs=[add_book_output])
    
    with gr.Tab("Add Review"):
        with gr.Row():
            book_id_input = gr.Textbox(label="Book ID")
            rating_input = gr.Slider(minimum=0, maximum=5, step=0.5, label="Rating")
        review_input = gr.Textbox(label="Review Text", lines=3)
        add_review_btn = gr.Button("Add Review")
        add_review_output = gr.Textbox(label="Result", interactive=False)
        add_review_btn.click(add_review_interface, 
                           inputs=[book_id_input, rating_input, review_input],
                           outputs=[add_review_output])
    
    with gr.Tab("View Books & Reviews"):
        with gr.Row():
            view_all_btn = gr.Button("View All Books and Reviews")
            refresh_btn = gr.Button("🔄 Refresh")
        view_output = gr.Textbox(label="Books and Reviews", interactive=False, lines=10)
        view_all_btn.click(view_all_books_reviews, inputs=[], outputs=[view_output])
        refresh_btn.click(view_all_books_reviews, inputs=[], outputs=[view_output])
    
    with gr.Tab("Delete"):
        gr.Markdown("### Delete Book")
        with gr.Row():
            del_book_input = gr.Textbox(label="Book ID")
            del_book_btn = gr.Button("Delete Book")
        del_book_output = gr.Textbox(label="Result", interactive=False)
        del_book_btn.click(delete_book_interface, inputs=[del_book_input], outputs=[del_book_output])
        
        gr.Markdown("### Delete Review")
        with gr.Row():
            del_review_book_input = gr.Textbox(label="Book ID")
            del_review_input = gr.Textbox(label="Review ID")
        del_review_btn = gr.Button("Delete Review")
        del_review_output = gr.Textbox(label="Result", interactive=False)
        del_review_btn.click(delete_review_interface, 
                           inputs=[del_review_book_input, del_review_input],
                           outputs=[del_review_output])

if __name__ == "__main__":
    demo.launch()