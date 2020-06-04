from .utils import get_provider_handler
from .yts import movie_search_api


def fetch_data(data):
    handler = get_provider_handler(data["provider"])
    if handler:
        return handler(data)
    return None


def search_handler(query):
    results = movie_search_api(query)
    return results
