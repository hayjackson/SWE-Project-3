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
            data = json.load(file)
           
            for i, show in enumerate(data["tv_shows"]):
                if 'id' not in show:
                    show['id'] = i + 1
            return data
    return {"tv_shows": []}

# Saving data to the JSON file
def save_data(data):
    with open(DATABASE_FILE, 'w') as file:
        json.dump(data, file, indent=4)



# Function to add tv_show
def add_show():
    data = load_data()
    title = input("Enter the TV show title: ")
    description = input("Enter the description: ")
    genre = input("Enter the genre: ")
    year = input("Enter the publication year: ")
    actors = input("Enter the main actors (comma-separated): ").split(',')
    rating = int(input("Enter the rating (1-5): "))
    
    show_id = max([show.get('id', 0) for show in data["tv_shows"]]) + 1
    
    show = {
        "id": show_id,
        "title": title,
        "description": description,
        "genre": genre,
        "year": year,
        "actors": [actor.strip() for actor in actors],
        "rating": rating
    }
    
    data["tv_shows"].append(show)
    save_data(data)
    print(f"Added: {title} (ID: {show_id})")

# Function to edit a TV show 
def edit_show():
    data = load_data()
    display_shows()
    show_id = int(input("Enter the ID of the show you want to edit: "))
    
    for show in data["tv_shows"]:
        if show["id"] == show_id:
            title = input("Enter the new title (or press Enter to keep current): ") or show['title']
            description = input("Enter the new description (or press Enter to keep current): ") or show['description']
            genre = input("Enter the new genre (or press Enter to keep current): ") or show['genre']
            year = input("Enter the new publication year (or press Enter to keep current): ") or show['year']
            actors = input("Enter the new main actors (comma-separated, or press Enter to keep current): ")
            actors = actors.split(',') if actors else show['actors']
            rating = input("Enter the new rating (1-5, or press Enter to keep current): ")
            rating = int(rating) if rating else show['rating']

            show.update({
                "title": title,
                "description": description,
                "genre": genre,
                "year": year,
                "actors": [actor.strip() for actor in actors],
                "rating": rating
            })
            save_data(data)
            print(f"Edited: {title} (ID: {show_id})")
            return
    print("Show not found")

# Function to delete a TV show
def delete_show():
    data = load_data()
    display_shows()
    show_id = int(input("Enter the ID of the show you want to delete: "))
    
    for index, show in enumerate(data["tv_shows"]):
        if show["id"] == show_id:
            deleted_show = data["tv_shows"].pop(index)
            save_data(data)
            print(f"Deleted: {deleted_show['title']} (ID: {show_id})")
            return
    print("Show not found")
# Function to display all TV shows
def display_shows():
    data = load_data()
    if not data["tv_shows"]:
        print("No TV shows in the list.")
    else:
        for show in data["tv_shows"]:
            show_id = show.get('id', 'N/A')
            print(f"ID: {show_id} - {show['title']} ({show['year']}) - Rating: {show['rating']}/5")
            print(f"   Genre: {show['genre']}")
            print(f"   Actors: {', '.join(show['actors'])}")
            print(f"   Description: {show['description']}")
            print()


# Function to search for TV shows using the TVmaze API
def search_shows(query):
    base_url = "http://api.tvmaze.com"
    response = requests.get(f"{base_url}/search/shows", params={"q": query})
    return response.json()

# Function to get TV show details from the TVmaze API
def get_show_details(show_id):
    base_url = "http://api.tvmaze.com"
    response = requests.get(f"{base_url}/shows/{show_id}?embed=cast")
    return response.json()

# Function to search and add a show using the API
def search_and_add_show():
    query = input("Enter the TV show name to search: ")
    results = search_shows(query)
    if results:
        show_id = results[0]['show']['id']
        details = get_show_details(show_id)
        title = details['name']
        description = details['summary'].replace('<p>', '').replace('</p>', '')
        genre = ', '.join(details['genres'])
        year = details['premiered'][:4] if details['premiered'] else 'N/A'
        actors = [actor['person']['name'] for actor in details['_embedded']['cast'][:3]]
        rating = int(input(f"Enter the rating for {title} (1-5): "))
        
        add_show_from_api(title, description, genre, year, actors, rating)
    else:
        print("No results found")

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
    print(f"Added: {title} (ID: {show_id})")

# Main menu
def main_menu():
    while True:
        print("\n--- TV Show Review App ---")
        print("1. Add a TV show manually")
        print("2. Search and add a TV show from API")
        print("3. Edit a TV show")
        print("4. Delete a TV show")
        print("5. Display all TV shows")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ")
        
        if choice == '1':
            add_show()
        elif choice == '2':
            search_and_add_show()
        elif choice == '3':
            edit_show()
        elif choice == '4':
            delete_show()
        elif choice == '5':
            display_shows()
        elif choice == '6':
            print("Thank you for using the TV Show Review App!")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the app
if __name__ == "__main__":
    main_menu()