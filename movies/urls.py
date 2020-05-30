from django.urls import path
from .views import *

urlpatterns = [
    path("", list_all_movies_view, name="list_movies"),
    path("<int:pk>", view_single_movie_view, name="view_movie"),
    path("add", add_movie_view, name="add_movie"),
    path("search", search_movies_view, name="search"),
]
