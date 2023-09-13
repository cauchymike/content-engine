import sqlite3

# Connect to the SQLite database or create a new one
conn = sqlite3.connect("mydatabase.db")

# Create a cursor object
cursor = conn.cursor()