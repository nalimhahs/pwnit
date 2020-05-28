from config import celery_app
from movies.models import Movie
from .services import *


@celery_app.task()
def start_movie_download(self, movie: Movie):

    deletable = movie.get_deletable_movies()
    running = get_all_torrents()
    for mov in deletable:
        if mov in running:
            delete_torrent(list(mov))
    try:
        if movie.get_current_slug_size() + movie.file_size > 100000:
            raise Exception("Storage full! Will retry in 5 mins.")
    except Exception:
        self.retry(cowntdown=300)

    download_from_magnet(movie.magnet_link)
    movie.set_status(Movie.DOWNLOADING)
