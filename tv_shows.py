#Author Mastewal 
# TV_shows
import sqlite3
import requests

DATABASE = 'tvshows_rvw.db'

# Function to add tv_show
def add_show_from_api(title, genre, rating):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO tv_shows (title, genre, rating)
        VALUES (?, ?, ?)
    ''', (title, genre, rating))
    
    show_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {"id": show_id, "title": title, "genre": genre, "rating": rating}
    
def get_show(show_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM tv_shows WHERE id = ?', (show_id,))
    show = cursor.fetchone()
    
    conn.close()
    
    if show:
        return {"id": show[0], "title": show[1], "genre": show[2], "rating": show[3]}
    
    return None


# Function to edit a TV show 
def edit_show(show_id, new_data):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    update_query = 'UPDATE tv_shows SET '
    update_data = []
    
    for key, value in new_data.items():
        update_query += f'{key} = ?, '
        update_data.append(value)

    update_query = update_query[:-2] + ' WHERE id = ?'
    
    update_data.append(show_id)
    
    cursor.execute(update_query, tuple(update_data))
    
    conn.commit()
    conn.close()
    
    return get_show(show_id)

# Function to delete a TV show
def delete_show(show_id):
    conn = sqlite3.connect(DATABASE)
    
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM tv_shows WHERE id = ?', (show_id,))
    
    deleted = cursor.rowcount > 0
    
    conn.commit()
    conn.close()
    
    return deleted


# Function to search for TV shows using the TVmaze API
def search_shows(query):
    base_url = "http://api.tvmaze.com"
    
    response = requests.get(f"{base_url}/search/shows", params={"q": query})
    
    if response.status_code == 200:
        return response.json()
    
    else:
        print("Error: unable to fetch shows")
        return []
    
    
#Filter by genre functionality 
def filter_shows_by_genre(genre):
    conn = sqlite3.connect(DATABASE)
    
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM tv_shows WHERE LOWER(genre) LIKE ?', (f'%{genre.lower()}%',))
    
    shows = cursor.fetchall()
    
    conn.close()
    
    return [{"id": show[0], "title": show[1], "genre": show[2], "rating": show[3]} for show in shows]
    
# Search for shows using the API
def search_and_add_show(query):
    search_results = search_shows(query)
    
    if not search_results:
        print(f"No results found for '{query}'")
        return None

   # Display search results
    print(f"Search results for '{query}':")
    for i, result in enumerate(search_results[:5], 1):
       show = result['show']
       print(f"{i}. {show['name']} ({show.get('premiered', 'N/A')[:4]})")

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

    selected_show = search_results[choice - 1]['show']
    title = selected_show['name']
    genre = ', '.join(selected_show.get('genres', []))
    rating = selected_show.get('rating', {}).get('average', 0)

    new_show = add_show_from_api(title, genre, rating)
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
           print(f"- {show['title']} ({show['rating']})")
