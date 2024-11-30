# Movies Database, Aditi Jha, November 29, 2024:

import mysql.connector

# Database connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        database="movies"
    )
