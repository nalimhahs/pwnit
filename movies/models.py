from django.db import models

# Create your models here.


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

    STATUS_CHOICES = [
        (0, "Created"),
        (1, "Waiting for download"),
        (2, "Downloading"),
        (3, "Download Completed"),
        (4, "Waiting for upload"),
        (5, "Uploading"),
        (6, "Upload Completed"),
        (7, "Ready for Watching"),
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

    def start_download(self):
        pass

    def start_upload(self):
        pass

    def cleanup_downloads(self):
        pass

    def generate_link(self):
        pass

    def __str__(self):
        return self.name + ":" + str(self.quality)
