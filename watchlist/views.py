from django.shortcuts import render
from django.http import HttpResponse
from . import database

def home_page_view(request):
    return render(request, 'home.html')

def add_user(request):
    message = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        if username:
            if database.add_user(username):
                message = "User added successfully!"
            else:
                message = "Failed to add user. Please try again."
        else:
            message = "Username cannot be empty."
    return render(request, 'add_user.html', {'message': message})

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
    users = database.all_users()
    return render(request, 'view_all_users.html', {'users': users})

def search_movies(request):
    if request.method == 'POST':
        search_term = request.POST.get('search_term')
        if search_term:
            movies = database.search_movies_api(search_term)
            return render(request, 'search_movies.html', {'movies': movies})
        else:
            return HttpResponse("Search term cannot be empty.")
    return render(request, 'search_movies.html')

def view_movie_details(request):
    if request.method == 'POST':
        search_term = request.POST.get('search_term')
        if search_term:
            movie_details = database.search_movies_api(search_term)
            return render(request, 'view_movie_details.html', {'movie_details': movie_details})
        else:
            return HttpResponse("Search term cannot be empty.")
    return render(request, 'view_movie_details.html')

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
