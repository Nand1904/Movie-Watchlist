from django.http import HttpResponse
from . import database
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .database import remove_watchlist_entries_for_user
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import CreateUserForm

def home_page_view(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account created successfully for ' + user)
            return redirect('login')
    else:
        form = CreateUserForm()
    return render(request, 'register.html', {'form': form})

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
           
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')
    
def logoutUser(request):
    logout(request)
    return redirect('login')

def delete_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            user.delete()
            remove_watchlist_entries_for_user(username)
            message = "User deleted successfully!"
            return redirect('home')
        else:
            message = "Invalid credentials. Please provide correct username, email, and password."
    else:
        message = ""
    
    return render(request, 'delete_user.html', {'message': message})

def view_all_users(request):
    users = database.all_users()
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

@login_required
def add_movie_to_watchlist(request, movie_id):
    if request.method == 'POST':
        user = request.user
        movie_details = database.get_movie_by_id(movie_id)  # Use a different variable for movie details
        if movie_details:
            if database.add_movie_to_watchlist(user.username, movie_id):  # Pass movie_id as integer
                return redirect('view_watchlist')
            else:
                return HttpResponse("Failed to add movie to watchlist. Please try again.")
        else:
            return HttpResponse("Movie details not found.")
    return HttpResponse("Invalid request method.")



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
