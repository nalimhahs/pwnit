from django.shortcuts import render, redirect
from .forms import AddMovieURLForm, MovieSearchForm
from scrapper.services import search_handler
from .models import Movie
from django.db.models import Q
from django.http import HttpResponseBadRequest


def search_online_movies_view(request):
    data = []
    if request.method == "POST":
        form = MovieSearchForm(request.POST)
        if form.is_valid():
            data = search_handler(form.cleaned_data["query"])
    else:
        form = MovieSearchForm()
    return render(request, "movies/add_movie.html", {"form": form, "data": data})


def list_all_movies_view(request):
    movies = Movie.objects.all()
    return render(request, "movies/list_movies.html", {"movies": movies})


def view_single_movie_view(request, pk):
    movie = Movie.objects.get(pk=pk)
    url = movie.generate_link()
    return render(request, "movies/view_movie.html", {"movie": movie, "url": url})


def search_local_movies_view(request):
    query = request.query_params.get("q", None)
    if not query:
        return HttpResponseBadRequest()
    movies = Movie.objects.filter(
        Q(name__unaccent__lower__trigram_similar=query)
        | Q(description__unaccent__lower__trigram_similar=query)
    )
    return render(request, "movies/search_result.html", {"movies": movies})
