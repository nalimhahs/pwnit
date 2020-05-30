from config import celery_app
from movies.models import Movie
from django.conf import settings

import requests


@celery_app.task()
def upload_movie(movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    movie.set_status(Movie.UPLOADING)
    response = requests.post(
        settings.STREAM_SERVER_URL + "/upload",
        data={"file_path": movie.file_location, "movie_id": movie.pk},
    )
    print(response)
    if response.status_code in (200, 201, 202):
        movie.set_status(Movie.UPLOAD_COMPLETE)
        movie.tel_message_id = response.content["message_id"]
        movie.set_status(Movie.READY)
    return movie


@celery_app.task()
def auto_upload_movie():
    downloaded = Movie.objects.filter(status=Movie.DOWNLOAD_COMPLETE)
    for movie in downloaded:
        upload_movie.delay(movie.pk)
    return {"downloaded": downloaded}
