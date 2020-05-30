from config import celery_app
from movies.models import Movie
from django.conf import settings

import requests


@celery_app.task()
def upload_movie(movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    response = requests.post(
        settings.STREAM_SERVER_URL + "/upload",
        data={"file_path": movie.file_location, "movie_id": movie.pk},
    )
    movie.tel_message_id = response.content["message_id"]
    movie.set_status(Movie.READY)
