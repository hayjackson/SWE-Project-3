# Movie tab Implementation:

import movies

def main():
    while True:
        print("\nMovie Review App")
        print("1. Add a Movie")
        print("2. Add a Review")
        print("3. Edit a Review")
        print("4. Delete a Review")
        print("5. Delete a Movie")  # New option for deleting a movie
        print("6. View All Reviews")
        print("7. Search Reviews by Movie ID")
        print("8. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            movie_name = input("Enter the movie name: ")
            movies.add_movie(movie_name)

        elif choice == "2":
            movie_id = int(input("Enter the movie ID: "))
            rating = int(input("Enter rating (0-5): "))
            note = input("Enter review note: ")
            movies.add_review(movie_id, rating, note)

        elif choice == "3":
            movie_id = int(input("Enter the movie ID: "))
            review_id = int(input("Enter the review ID: "))
            rating = input("Enter new rating (leave blank to keep current): ")
            note = input("Enter new note (leave blank to keep current): ")
            rating = int(rating) if rating else None
            note = note if note else None
            movies.edit_review(movie_id, review_id, rating, note)

        elif choice == "4":
            movie_id = int(input("Enter the movie ID: "))
            review_id = int(input("Enter the review ID to delete: "))
            movies.delete_review(movie_id, review_id)

        elif choice == "5":  
            movie_id = int(input("Enter the movie ID to delete: "))
            movies.delete_movie(movie_id)

        elif choice == "6":
            movies.view_reviews()

        elif choice == "7":
            movie_id = int(input("Enter the movie ID to search: "))
            movies.search_reviews(movie_id)

        elif choice == "8":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
