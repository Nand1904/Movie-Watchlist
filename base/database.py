from sqlite3 import Cursor
import requests
import traceback
from django.db import connection
from django.core.management import call_command
from django.db.utils import ConnectionDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from .models import Watchlist
from django.contrib.auth.models import User

# API details
API_KEY = '8b76ff1a2bbd88072cc966292315c565'
BASE_URL = 'https://api.themoviedb.org/3'

def search_movies_api(search_term):
    try:
        url = f"{BASE_URL}/search/movie?api_key={API_KEY}&query={search_term}"
        response = requests.get(url)
        if response.status_code == 200:
            results = response.json().get('results', [])
            for movie in results:
                movie_id = movie['id']
                image_url = f"{BASE_URL}/movie/{movie_id}/images?api_key={API_KEY}"
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    images = image_response.json()
                    posters = [img['file_path'] for img in images.get('posters', [])]
                    movie['poster'] = posters[0] if posters else None
            return results
        else:
            print("Error: Unable to fetch movies from the API.")
            return []
    except Exception as e:
        print(f"Error searching movies in API: {e}")
        return []

def get_movie_by_id(movie_id):
    try:
        url = f"{BASE_URL}/movie/{movie_id}?api_key={API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            movie = response.json()
            image_url = f"{BASE_URL}/movie/{movie_id}/images?api_key={API_KEY}"
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                images = image_response.json()
                posters = [img['file_path'] for img in images.get('posters', [])]
                movie['poster'] = posters[0] if posters else None
            return movie
        else:
            print(f"Error: Unable to fetch movie with id {movie_id} from the API.")
            return None
    except Exception as e:
        print(f"Error fetching movie from API: {e}")
        return None

# USER MANAGEMENT
def add_user(username):
    try:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO Users (username) VALUES (?)", (username,))
            print(f"User '{username}' added.")
            return True
    except Exception as e:
        print(f"Error adding user to database: {e}")
        return False

def delete_user(username):
    try:
        # Check if the user exists
        Cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
        existing_user = Cursor.fetchone()

        if not existing_user:
            print(f"User '{username}' does not exist.")
            return False

        # Delete user from the database
        Cursor.execute("DELETE FROM Users WHERE username = ?", (username,))
        connection.commit()
        
        # Delete associated watchlist entries for the user
        Cursor.execute("DELETE FROM Watchlist WHERE user_id = ?", (existing_user[0],))
        connection.commit()

        print(f"User '{username}' deleted.")
        return True
    except Exception as e:
        print(f"Error deleting user: {e}")
        return False

def all_users():
    try:
        Cursor.execute("SELECT * FROM Users")
        return Cursor.fetchall()
    except Exception as e:
        print(f"Error fetching users from database: {e}")
        return []

# WATCHLIST MANAGEMENT
def add_movie_to_watchlist(username, movie): # Completed
    try:
        movie_title = movie.get('original_title', 'N/A')
        movie_release_date = movie.get('release_date', 'N/A')
        movie_adult = movie.get('adult', 'N/A')
        movie_rating = movie.get('vote_average', 'N/A')
        movie_overview = movie.get('overview', 'N/A')
        movie_poster = movie.get('poster', 'N/A')
        movie_id = movie.get('id', 'N/A')

        # Check if the movie is already in the watchlist for the user
        existing_entry = Watchlist.objects.filter(username=username, movie_title=movie_title)

        if existing_entry.exists():
            print(f"Movie '{movie_title}' already exists in the watchlist.")
            return False

        # Add movie to watchlist
        Watchlist.objects.create(
            username=username,
            movie_id=movie_id,
            movie_title=movie_title,
            release_date=movie_release_date,
            adult=movie_adult,
            rating=movie_rating,
            overview=movie_overview,
            movie_poster=movie_poster
        )
        print(f"Movie '{movie_title}' added to the watchlist.")
        return True
    except Exception as e:
        print(f"Error adding movie to watchlist: {type(e).__name__}, {e}")
        return False


def user_exists(username):
    try:
        Cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
        existing_user = Cursor.fetchone()
        return existing_user is not None
    except Exception as e:
        print(f"Error checking if user exists: {e}")
        return False

def remove_movie_from_watchlist(username, movie_title):
    try:
        # Check if the user exists
        user = User.objects.get(username=username)
        
        # Check if the movie exists in the user's watchlist
        watchlist_entry = Watchlist.objects.filter(user=user, movie_title=movie_title).first()
        if watchlist_entry:
            # Remove the movie from the user's watchlist
            watchlist_entry.delete()
            print(f"Movie '{movie_title}' removed from the watchlist for user '{username}'.")
            return True
        else:
            print(f"Movie '{movie_title}' not found in the watchlist for user '{username}'.")
            return False
    except Exception as e:
        print(f"Error removing movie from watchlist: {e}")
        return False


# def movie_exists_in_watchlist(username, movie_name):
#     try:
#         # Check if the user exists
#         Cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
#         existing_user = Cursor.fetchone()

#         if not existing_user:
#             print(f"User '{username}' does not exist.")
#             return False

#         # Check if the movie exists in the user's watchlist
#         Cursor.execute("SELECT * FROM Watchlist WHERE user_id = ? AND movie_name = ?", (existing_user[0], movie_name))
#         existing_movie = Cursor.fetchone()
#         return existing_movie is not None
#     except Exception as e:
#         print(f"Error checking if movie exists in watchlist: {e}")
#         return False

def get_watchlist(username):
    try:
        watchlist = Watchlist.objects.filter(username=username)
        return [model_to_dict(movie) for movie in watchlist]
    except Exception as e:
        print(f"Error fetching watchlist: {e}")
        return None
    
def remove_watchlist_entries_for_user(username):
    try:
        # Get the user's ID
        Cursor.execute("SELECT id FROM Users WHERE username = ?", (username,))
        user_id = Cursor.fetchone()

        if user_id is not None:
            # Remove watchlist entries for the user
            Cursor.execute("DELETE FROM Watchlist WHERE user_id = ?", (user_id[0],))
            connection.commit()
            print(f"Watchlist entries removed for user '{username}'.")
        else:
            print(f"User '{username}' does not exist.")
    except Exception as e:
        print(f"Error removing watchlist entries for user '{username}': {e}")