import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("pwnit")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "auto_update_download_status": {
        "task": "torrent_client.tasks.auto_update_download_status",
        "schedule": 10,
    },
    "auto_delete_completed": {
        "task": "torrent_client.tasks.auto_delete_completed",
        "schedule": 30,
    },
    "auto_upload_completed": {
        "task": "tel_storage.tasks.auto_upload_movie",
        "schedule": 30,
    },
}
