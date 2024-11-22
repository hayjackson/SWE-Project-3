#Author Mastewal 
# TV_shows
import requests 
import json
import os

# JSON file to store data
DATABASE_FILE = 'tv_shows.json'

# Loading data from the JSON file
def load_data():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'r') as file:
            return json.load(file)
    return {"tv_shows": []}

    
# Saving data to the JSON file
def save_data(data):
    with open(DATABASE_FILE, 'w') as file:
        json.dump(data, file, indent=4)



# Function to add tv_show
def add_show_from_api(title, description, genre, year, actors, rating):
    data = load_data()
    show_id = max([show.get('id', 0) for show in data["tv_shows"]]) + 1
    show = {
        "id": show_id,
        "title": title,
        "description": description,
        "genre": genre,
        "year": year,
        "actors": actors,
        "rating": rating
    }
    data["tv_shows"].append(show)
    save_data(data)
    return show


def get_show(show_id):
    data = load_data()
    for show in data["tv_shows"]:
        if show["id"] == show_id:
            return show
    return None

# Function to edit a TV show 
def edit_show(show_id, new_data):
    data = load_data()
    for show in data["tv_shows"]:
        if show["id"] == show_id:
            show.update(new_data)
            save_data(data)
            return show
    return None

# Function to delete a TV show
def delete_show(show_id):
    data = load_data()
    for index, show in enumerate(data["tv_shows"]):
        if show["id"] == show_id:
            del data["tv_shows"][index]
            save_data(data)
            return True
    return False


# Function to search for TV shows using the TVmaze API
def search_shows(query):
    base_url = "http://api.tvmaze.com"
    response = requests.get(f"{base_url}/search/shows", params={"q": query})
    if response.status_code == 200:
        return response.json()
    else:
        print("Error: unable to fetch shows")
        return  []
    
#Filter by genre functionality 
def filter_shows_by_genre(genre):
    data = load_data()
    filtered_shows = [show for show in data["tv_shows"] if genre.lower() in show["genre"].lower()]
    return filtered_shows
    
def search_and_add_show(query):
    # Search for shows using the API
    search_results = search_shows(query)
    
    if not search_results:
        print(f"No results found for '{query}'")
        return None

    # Display search results
    print(f"Search results for '{query}':")
    for i, result in enumerate(search_results[:5], 1):  # Limit to top 5 results
        show = result['show']
        print(f"{i}. {show['name']} ({show.get('premiered', 'N/A')[:4]})")

    # Ask user to select a show
    while True:
        try:
            choice = int(input("Enter the number of the show you want to add (0 to cancel): "))
            if 0 <= choice <= len(search_results):
                break
            print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

    if choice == 0:
        return None

    # Get the selected show
    selected_show = search_results[choice - 1]['show']

    # Extract relevant information
    title = selected_show['name']
    description = selected_show.get('summary', '').replace('<p>', '').replace('</p>', '')
    genre = ', '.join(selected_show.get('genres', []))
    year = selected_show.get('premiered', '')[:4]
    actors = ', '.join([actor['person']['name'] for actor in selected_show.get('_embedded', {}).get('cast', [])[:3]])
    rating = selected_show.get('rating', {}).get('average', 0)

    # Add the show to the database
    new_show = add_show_from_api(title, description, genre, year, actors, rating)
    print(f"Added: {new_show['title']}")
    return new_show

def display_shows_by_genre():
    genre = input("Enter the genre to filter by: ")
    filtered_shows = filter_shows_by_genre(genre)
    
    if not filtered_shows:
        print(f"No shows found in the '{genre}' genre.")
    else:
        print(f"Shows in the '{genre}' genre:")
        for show in filtered_shows:
            print(f"- {show['title']} ({show['year']})")
