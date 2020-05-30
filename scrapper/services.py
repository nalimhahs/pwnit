from .utils import get_url_handler


def fetch_data(url):
    handler = get_url_handler(url)
    if handler:
        return handler(url)
    return None
