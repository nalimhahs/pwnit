#!/bin/sh
# qbittorrent-nox &
python -m stream_server &
gunicorn config.asgi --bind 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker --reload
