from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page_view, name='home'),
    path('add_user/', views.add_user, name='add_user'),
    path('delete_user/', views.delete_user, name='delete_user'),
    path('view_all_users/', views.view_all_users, name='view_all_users'),
    path('search_movies/', views.search_movies, name='search_movies'),
    path('view_movie_details/', views.view_movie_details, name='view_movie_details'),
    path('add_movie_to_watchlist/', views.add_movie_to_watchlist, name='add_movie_to_watchlist'),
    path('view_watchlist/', views.view_watchlist, name='view_watchlist'),
    path('remove_movie_from_watchlist/', views.remove_movie_from_watchlist, name='remove_movie_from_watchlist'),
]