from django.urls import path
from .views import *
from movies.api.views import add_movie_api_view
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("", list_all_movies_view, name="list_movies"),
    path("<int:pk>", view_single_movie_view, name="view_movie"),
    path("add", search_online_movies_view, name="add_movie"),
    path("search", search_local_movies_view, name="search"),
    path("api/add", csrf_exempt(add_movie_api_view.as_view())),
]
