from django.shortcuts import render, redirect
from .forms import AddMovieURLForm
from scrapper.tasks import add_movie
from .models import Movie

# Create your views here.


def add_movie_view(request):
    if request.method == "POST":
        form = AddMovieURLForm(request.POST)
        if form.is_valid():
            add_movie.delay(form.url)
    else:
        form = AddMovieURLForm()
    return render(request, "movies/add_movie.html", {"form": form})


def list_all_movies_view(request):
    movies = Movie.objects.all()
    return render(request, "movies/list_movies.html", {"movies": movies})


def view_single_movie_view(request, id):
    movie = Movie.objects.get(pk=id)
    return render(request, "movies/view_movie.html", {"movie": movie})
