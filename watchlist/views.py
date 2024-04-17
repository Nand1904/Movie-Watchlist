from sqlite3 import Cursor
from django.http import HttpResponse
from . import database
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import CreateUserForm
def home_page_view(request):
    return render(request, 'home.html')
from .database import conn  # Import the connection object from the database module

def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account created successfully for ' + user)  # Display success message
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = CreateUserForm()
    return render(request, 'register.html', {'form': form})

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
           
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Fix here: Use the authenticated user object
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect')  # Fix here: Use messages.error
            return render(request, 'login.html')  # Fix here: Render login.html again
    else:
        return render(request, 'login.html')
    
def logoutUser(request):
    logout(request)
    return redirect('login')

def delete_user(request):
    message = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        if username:
            if database.delete_user(username):
                message = "User deleted successfully!"
            else:
                message = "Failed to delete user. Please try again."
        else:
            message = "Username cannot be empty."
    return render(request, 'delete_user.html', {'message': message})

def view_all_users(request):
    users = User.objects.all()  # Retrieve all users from the Django database
    return render(request, 'view_all_users.html', {'users': users})

def search_movies(request):
    search_term = request.GET.get('q', '')
    if search_term:
        movies = database.search_movies_api(search_term)
        return render(request, 'search_movies.html', {'movies': movies})
    else:
        return render(request, 'search_movies.html')

def view_movie_details(request, movie_id):
    movie = database.get_movie_by_id(movie_id)
    if movie:
        context = {
            'movie_details': {
                'title': movie.get('original_title', 'N/A'),
                'release_date': movie.get('release_date', 'N/A'),
                'adult': movie.get('adult', 'N/A'),
                'rating': movie.get('vote_average', 'N/A'),
                'overview': movie.get('overview', 'N/A'),
                'poster': movie.get('poster', 'N/A')
            }
        }
    else:
        context = {'movie_details': None}
    return render(request, 'view_movie_details.html', context)

def add_movie_to_watchlist(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        movie_name = request.POST.get('movie_name')
        if username and movie_name:
            if database.add_movie_to_watchlist(username, movie_name):
                return HttpResponse("Movie added to watchlist successfully!")
            else:
                return HttpResponse("Failed to add movie to watchlist. Please try again.")
        else:
            return HttpResponse("Username and movie name cannot be empty.")
    return render(request, 'add_movie_to_watchlist.html')

def view_watchlist(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if username:
            watchlist = database.get_watchlist(username)
            return render(request, 'view_watchlist.html', {'watchlist': watchlist, 'username': username})
        else:
            return HttpResponse("Username cannot be empty.")
    return render(request, 'view_watchlist.html')

def remove_movie_from_watchlist(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        movie_name = request.POST.get('movie_name')
        if username and movie_name:
            if database.remove_movie_from_watchlist(username, movie_name):
                return HttpResponse("Movie removed from watchlist successfully!")
            else:
                return HttpResponse("Failed to remove movie from watchlist. Please try again.")
        else:
            return HttpResponse("Username and movie name cannot be empty.")
    return render(request, 'remove_movie_from_watchlist.html')
