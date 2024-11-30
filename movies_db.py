# Movies Database, Aditi Jha, November 29, 2024:

import mysql.connector

# Database connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="ajha26@wooster.edu",  
        password="26Aj@2003",  
        database="movies"
    )
