from .yts import fetch_data as yts

AVAILABLE_HOSTS = [
    ("yts", yts),
]


def get_domain(url):
    spltAr = url.split("://")
    i = (0, 1)[len(spltAr) > 1]
    dm = spltAr[i].split("?")[0].split("/")[0].split(":")[0].lower().split(".")[0]
    return dm


def get_url_handler(url):
    host = get_domain(url)
    for h in AVAILABLE_HOSTS:
        if host == h[0]:
            return h[1]
    return None
