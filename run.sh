#!/bin/sh
qbittorrent-nox &
python -m stream_server &
celery -A config worker --loglevel=info
celery -A config beat --loglevel=info
gunicorn config.asgi --bind 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker --reload
