#!/bin/sh
# qbittorrent-nox &
gunicorn config.asgi --bind 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker --reload
