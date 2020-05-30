from config import celery_app
from movies.models import Movie
from .services import fetch_data


@celery_app.task()
def add_movie(self, url):
    # run script to get data
    data = fetch_data(url)
    if data:
        Movie.objects.create(data)
    else:
        print("Invalid url")
