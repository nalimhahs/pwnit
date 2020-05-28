from urllib.parse import parse_qs, urlparse

from django.db import models
from django.db.models import Q

from torrent_client.tasks import start_movie_download


class Movie(models.Model):

    # Possible states
    CREATED = 0
    WAITING_DOWNLOAD = 1
    DOWNLOADING = 2
    DOWNLOAD_COMPLETE = 3
    WAITING_UPLOAD = 4
    UPLOADING = 5
    UPLOAD_COMPLETE = 6
    READY = 7
    INVALID = 8

    STATUS_CHOICES = [
        (0, "Created"),
        (1, "Waiting for download"),
        (2, "Downloading"),
        (3, "Download Completed"),
        (4, "Waiting for upload"),
        (5, "Uploading"),
        (6, "Upload Completed"),
        (7, "Ready for Watching"),
        (8, "Invalid"),
    ]

    QUALITY_CHOICES = [
        (240, "240p"),
        (360, "360p"),
        (480, "480p"),
        (720, "720p"),
        (1080, "1080p"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    thumbnail = models.ImageField()
    quality = models.IntegerField(choices=QUALITY_CHOICES)
    file_size = models.PositiveIntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now_add=True)
    restricted = models.BooleanField(default=False)
    imdb_url = models.URLField(blank=True, null=True)
    file_location = models.CharField(max_length=1024, blank=True, null=True)
    length = models.TimeField(blank=True, null=True)

    # Telegram Message id
    tel_message_id = models.IntegerField(null=True, blank=True, editable=False)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    magnet_link = models.CharField(max_length=512)

    def set_status(self, status):
        self.status = status

    def start_download(self):
        if self.file_size <= 1500:
            self.set_status(self.WAITING_DOWNLOAD)
            start_movie_download.delay(self)
        else:
            self.set_status(self.INVALID)

    def start_upload(self):
        pass

    def cleanup_downloads(self):
        pass

    def get_info_hash(self):
        xts = parse_qs(urlparse(self.magnet_link).query)["xt"]
        _, x = xts[0].split(":")
        _, info_hash = x.split(":")
        return info_hash

    def generate_link(self):
        pass

    @staticmethod
    def get_current_slug_size():
        downloads = Movie.objects.filter(
            Q(status=Movie.DOWNLOADING) | Q(status=Movie.DOWNLOAD_COMPLETE)
        )
        size = 0
        for movie in downloads:
            size += movie.file_size
        return size

    @staticmethod
    def get_deletable_hashes():
        upload_complete = Movie.objects.filter(status=Movie.UPLOAD_COMPLETE)
        deletable = []
        for movie in upload_complete:
            deletable.append({"movie": movie, "hash": movie.get_info_hash()})
        return deletable

    @staticmethod
    def get_downloading_hashes():
        downloading = Movie.objects.filter(status=Movie.DOWNLOADING)
        d = []
        for movie in downloading:
            d.append({"movie": movie, "hash": movie.get_info_hash()})
        return d

    def __str__(self):
        return self.name + ":" + str(self.quality)
