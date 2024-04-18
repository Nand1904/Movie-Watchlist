from django.urls import path
from base import views  # Import your views module

urlpatterns = [
    path('', views.home_page_view, name='home'),  # Define the root URL pattern here
    path('register/', views.register, name='register'), # Define the URL pattern for the register view here')
    path('login/', views.loginPage, name='login'), # Define the URL pattern for the login view here
    path('logout/', views.logoutUser, name='logout'), # Define the URL pattern for the logout view her
    path('delete_user/', views.delete_user, name='delete_user'), # Define the URL pattern for the delete_user view here
    path('search_movies/', views.search_movies, name='search_movies'), # Define the URL pattern for the search_movies view here
    path('view_movie_details/<int:movie_id>/', views.view_movie_details, name='view_movie_details'), # Define the URL pattern for the view_movie_details view here
    path('add_movie_to_watchlist/<str:username>/<int:movie_id>/', views.add_movie_to_watchlist, name='add_movie_to_watchlist'),  # Define the URL pattern for the add_movie_to_watchlist view here
    path('view_watchlist/<str:username>/', views.view_watchlist, name='view_watchlist'), # Define the URL pattern for the view_watchlist view here
    path('remove_movie_from_watchlist/', views.remove_movie_from_watchlist, name='remove_movie_from_watchlist'), # Define the URL pattern for the remove_movie_from_watchlist view here
    # Add URL patterns for the remaining views here
]