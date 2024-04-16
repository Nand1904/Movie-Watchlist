import pyodbc
import requests

# Connect to SQL Server
conn = pyodbc.connect('DRIVER={SQL SERVER};SERVER=DINI\SQLEXPRESS;DATABASE=WATCHLIST;')
cursor = conn.cursor()

# API details
API_KEY = '8b76ff1a2bbd88072cc966292315c565'
BASE_URL = 'https://api.themoviedb.org/3'

# MOVIE MANAGEMENT
def search_movies_api(search_term):
    try:
        url = f"{BASE_URL}/search/movie?api_key={API_KEY}&query={search_term}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get('results', [])
        else:
            print("Error: Unable to fetch movies from the API.")
            return []
    except Exception as e:
        print(f"Error searching movies in API: {e}")
        return []

# USER MANAGEMENT
def add_user(username):
    try:
        cursor.execute("INSERT INTO Users (username) VALUES (?)", (username,))
        conn.commit()
        print(f"User '{username}' added.")
        return True
    except Exception as e:
        print(f"Error adding user to database: {e}")
        return False

def delete_user(username):
    try:
        # Check if the user exists
        cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()

        if not existing_user:
            print(f"User '{username}' doe not exist.")
            return False

        # Delete user from the database
        cursor.execute("DELETE FROM Users WHERE username = ?", (username,))
        conn.commit()
        
        # Delete associated watchlist entries for the user
        cursor.execute("DELETE FROM Watchlist WHERE user_id = ?", (existing_user[0],))
        conn.commit()

        print(f"User '{username}' deleted.")
        return True
    except Exception as e:
        print(f"Error deleting user: {e}")
        return False


def all_users():
    try:
        cursor.execute("SELECT * FROM Users")
        return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching users from database: {e}")
        return []

# WATCHLIST MANAGEMENT
def add_movie_to_watchlist(username, movie_name):
    try:
        # Check if the movie is already in the watchlist for the user
        cursor.execute("SELECT * FROM Watchlist WHERE user_id = (SELECT id FROM Users WHERE username = ?) AND movie_name = ?", (username, movie_name))
        existing_entry = cursor.fetchone()

        if existing_entry:
            print(f"Movie '{movie_name}' already exists in the watchlist.")
            return False

        # Add movie to watchlist
        cursor.execute("INSERT INTO Watchlist (user_id, movie_name) VALUES ((SELECT id FROM Users WHERE username = ?), ?)", (username, movie_name))
        conn.commit()
        print(f"Movie '{movie_name}' added to the watchlist.")
        return True
    except Exception as e:
        print(f"Error adding movie to watchlist: {e}")
        return False

def user_exists(username):
    try:
        cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()
        return existing_user is not None
    except Exception as e:
        print(f"Error checking if user exists: {e}")
        return False

def remove_movie_from_watchlist(username, movie_name):
    try:
        cursor.execute("SELECT id FROM Users WHERE username = ?", (username,))
        user_id = cursor.fetchone()

        if user_id is None:
            print(f"User '{username}' does not exist.")
            return False

        # Remove movie from watchlist
        cursor.execute("DELETE FROM Watchlist WHERE user_id = ? AND movie_name = ?", (user_id[0], movie_name))
        conn.commit()
        print(f"Movie '{movie_name}' removed from the watchlist.")
        return True
    except Exception as e:
        print(f"Error removing movie from watchlist: {e}")
        return False

def movie_exists_in_watchlist(username, movie_name):
    try:
        # Check if the user exists
        cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()

        if not existing_user:
            print(f"User '{username}' does not exist.")
            return False

        # Check if the movie exists in the user's watchlist
        cursor.execute("SELECT * FROM Watchlist WHERE user_id = ? AND movie_name = ?", (existing_user[0], movie_name))
        existing_movie = cursor.fetchone()
        return existing_movie is not None
    except Exception as e:
        print(f"Error checking if movie exists in watchlist: {e}")
        return False

def get_watchlist(username):
    try:
        cursor.execute("SELECT movie_name FROM Watchlist WHERE user_id = (SELECT id FROM Users WHERE username = ?)", (username,))
        watchlist = cursor.fetchall()
        return watchlist
    except Exception as e:
        print(f"Error fetching watchlist: {e}")
        return None