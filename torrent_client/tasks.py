from config import celery_app
from .services import *
from django.conf import settings

from movies.models import Movie
from tel_storage.tasks import upload_movie


@celery_app.task(bind=True)
def start_movie_download(self, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    delete_old = auto_delete_completed
    delete_old.wait(timeout=None, interval=0.5)

    try:
        if Movie.get_current_slug_size() + movie.file_size > settings.MAX_SLUG_SIZE:
            raise Exception("Storage full! Will retry in 5 mins.")
    except Exception:
        self.retry(cowntdown=300)

    download_from_magnet(movie.magnet_link)
    movie.set_status(Movie.DOWNLOADING)


# Periodic task: every 5-10 secs?
@celery_app.task()
def auto_update_download_status():
    downloading = Movie.get_downloading_hashes()
    modified = []
    for mov in downloading:
        if check_if_torrent_complete(mov["hash"]):
            mov["movie"].set_status(Movie.DOWNLOAD_COMPLETE)
            upload_movie(mov["movie"].pk)
            modified.append(mov["movie"])
    return modified


# Periodic task: every 30 secs?
@celery_app.task()
def auto_delete_completed():
    deletable = Movie.get_deletable_hashes()
    running = get_all_torrent_hashes()
    deleted = []
    for mov in deletable:
        if mov in running:
            delete_torrent(mov["hash"])
            mov["movie"].set_status(Movie.READY)
            deleted.append(mov["movie"])
    return deleted
