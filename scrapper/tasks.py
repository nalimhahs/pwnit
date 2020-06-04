from config import celery_app
from movies.models import Movie
from .services import fetch_data
from torrent_client.tasks import start_movie_download


@celery_app.task()
def add_movie(data):
    # run script to get data
    obj_data = fetch_data(data)
    if obj_data:
        movie = Movie.objects.create(**obj_data)
        if movie.file_size <= 1500:
            movie.set_status(movie.WAITING_DOWNLOAD)
            start_movie_download.delay(movie.pk)
        else:
            movie.set_status(movie.INVALID)
    else:
        print("Invalid url")
