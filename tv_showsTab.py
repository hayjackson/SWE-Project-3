import tv_shows

import gradio as gr
import json
import os

# Using the same database file as the backend
DATABASE_FILE = 'tv_show_reviews.json'

# Loading and saving functions remain the same
def load_data():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'r') as file:
            return json.load(file)
    return {"shows": []}

def save_data(data):
    with open(DATABASE_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Core functions updated for TV shows
def add_show_interface(show_title):
    if not show_title.strip():
        return "❌ Error: Show title cannot be empty!"
    try:
        data = load_data()
        show = {
            "id": len(data["shows"]) + 1,
            "title": show_title,
            "reviews": []
        }
        data["shows"].append(show)
        save_data(data)
        return f"✅ Success: '{show_title}' added to your library!"
    except Exception as e:
        return f"❌ Error: Failed to add show - {str(e)}"

def add_review_interface(show_id, rating, review_text):
    try:
        show_id = int(show_id)
        rating = float(rating)
        if not (0 <= rating <= 5):
            return "❌ Error: Rating must be between 0 and 5!"
        
        data = load_data()
        for show in data["shows"]:
            if show["id"] == show_id:
                review_id = len(show["reviews"]) + 1
                review = {
                    "review_id": review_id,
                    "rating": rating,
                    "note": review_text
                }
                show["reviews"].append(review)
                save_data(data)
                return f"✅ Review successfully added to '{show['title']}'"
        return f"❌ Error: Show with ID {show_id} not found!"
    except ValueError:
        return "❌ Error: Invalid show ID or rating format!"
    except Exception as e:
        return f"❌ Error: Failed to add review - {str(e)}"

def view_all_shows_reviews():
    try:
        data = load_data()
        if not data["shows"]:
            return "📺 Your TV show library is empty. Add some shows to get started!"
        
        output = []
        output.append("╔══════════════════════════════════════╗")
        output.append("║       📺 YOUR TV SHOW LIBRARY 📺      ║")
        output.append("╚══════════════════════════════════════╝\n")
        
        for show in data["shows"]:
            output.append(f"📺 Show #{show['id']} | {show['title']}")
            if not show["reviews"]:
                output.append("   💭 No reviews yet")
            else:
                for review in show["reviews"]:
                    stars = "⭐" * int(review['rating'])
                    half_star = "✨" if review['rating'] % 1 >= 0.5 else ""
                    output.append(f"\n   Review #{review['review_id']}")
                    output.append(f"   Rating: {stars}{half_star} ({review['rating']}/5)")
                    output.append(f"   📝 {review['note']}")
            output.append("\n" + "─" * 50 + "\n")
        
        return "\n".join(output)
    except Exception as e:
        return f"❌ Error: Failed to load reviews - {str(e)}"

def delete_show_interface(show_id):
    try:
        show_id = int(show_id)
        data = load_data()
        initial_length = len(data["shows"])
        data["shows"] = [show for show in data["shows"] if show["id"] != show_id]
        if len(data["shows"]) == initial_length:
            return f"❌ Error: Show #{show_id} not found!"
        save_data(data)
        return f"✅ Show #{show_id} and its reviews have been removed."
    except ValueError:
        return "❌ Error: Invalid show ID format!"
    except Exception as e:
        return f"❌ Error: Failed to delete show - {str(e)}"

def delete_review_interface(show_id, review_id):
    try:
        show_id = int(show_id)
        review_id = int(review_id)
        data = load_data()
        for show in data["shows"]:
            if show["id"] == show_id:
                initial_length = len(show["reviews"])
                show["reviews"] = [r for r in show["reviews"] if r["review_id"] != review_id]
                if len(show["reviews"]) == initial_length:
                    return f"❌ Error: Review #{review_id} not found!"
                save_data(data)
                return f"✅ Review #{review_id} removed from '{show['title']}'"
        return f"❌ Error: Show #{show_id} not found!"
    except ValueError:
        return "❌ Error: Invalid show ID or review ID format!"
    except Exception as e:
        return f"❌ Error: Failed to delete review - {str(e)}"

# Create the enhanced Gradio interface
with gr.Blocks(
    title="TV Show Review Manager",
    theme=gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="indigo",
        neutral_hue="slate",
        font=gr.themes.GoogleFont("Poppins")
    )
) as demo:
    gr.Markdown(
        """
        # 📺 TV Show Review Manager
        Keep track of your favorite TV shows and share your thoughts on them!
        
        ---
        """
    )
    
    with gr.Tab("📺 Add Show"):
        gr.Markdown("### Add a New TV Show to Your Library")
        with gr.Row():
            show_input = gr.Textbox(
                label="TV Show Title",
                placeholder="Enter the title of the TV show...",
                scale=3
            )
            add_show_btn = gr.Button("📺 Add Show", scale=1, variant="primary")
        add_show_output = gr.Textbox(label="Status", interactive=False)
        add_show_btn.click(add_show_interface, inputs=[show_input], outputs=[add_show_output])
    
    with gr.Tab("⭐ Add Review"):
        gr.Markdown("### Share Your Thoughts")
        with gr.Row():
            show_id_input = gr.Textbox(
                label="Show ID",
                placeholder="Enter the show's ID number...",
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
            placeholder="Share your thoughts about the show...",
            lines=3
        )
        add_review_btn = gr.Button("⭐ Add Review", variant="primary")
        add_review_output = gr.Textbox(label="Status", interactive=False)
        add_review_btn.click(
            add_review_interface, 
            inputs=[show_id_input, rating_input, review_input],
            outputs=[add_review_output]
        )
    
    with gr.Tab("📚 View Library"):
        with gr.Row():
            view_all_btn = gr.Button("📺 View All Shows", scale=2, variant="primary")
            refresh_btn = gr.Button("🔄 Refresh", scale=1)
        view_output = gr.Textbox(
            label="Your TV Show Library",
            interactive=False,
            lines=15,
            show_copy_button=True
        )
        view_all_btn.click(view_all_shows_reviews, inputs=[], outputs=[view_output])
        refresh_btn.click(view_all_shows_reviews, inputs=[], outputs=[view_output])
    
    with gr.Tab("🗑️ Manage"):
        with gr.Row():
            gr.Markdown(
                """
                ### Remove Show
                Delete a show and all its reviews from your library
                """
            )
        with gr.Row():
            del_show_input = gr.Textbox(
                label="Show ID",
                placeholder="Enter the show's ID number...",
                scale=3
            )
            del_show_btn = gr.Button("🗑️ Delete Show", scale=1, variant="secondary")
        del_show_output = gr.Textbox(label="Status", interactive=False)
        del_show_btn.click(delete_show_interface, inputs=[del_show_input], outputs=[del_show_output])
        
        gr.Markdown("---")
        
        with gr.Row():
            gr.Markdown(
                """
                ### Remove Review
                Delete a specific review from a show
                """
            )
        with gr.Row():
            del_review_show_input = gr.Textbox(
                label="Show ID",
                placeholder="Enter the show's ID number...",
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
            inputs=[del_review_show_input, del_review_input],
            outputs=[del_review_output]
        )

if __name__ == "__main__":
    demo.launch()
