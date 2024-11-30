# Movies Database, Aditi Jha, November 29, 2024:

import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables from the m.env file
load_dotenv("m.env")

# Database connection
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
