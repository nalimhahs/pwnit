from urllib.parse import parse_qs, urlparse, quote_plus


AVAILABLE_TRACKERS = [
    "udp://glotorrents.pw:6969/announce",
    "udp://tracker.opentrackr.org:1337/announce",
    "udp://torrent.gresille.org:80/announce",
    "udp://tracker.openbittorrent.com:80",
    "udp://tracker.coppersurfer.tk:6969",
    "udp://tracker.leechers-paradise.org:6969",
    "udp://p4p.arenabg.ch:1337",
    "udp://tracker.internetwarriors.net:1337",
]


def get_domain(url):
    spltAr = url.split("://")
    i = (0, 1)[len(spltAr) > 1]
    dm = spltAr[i].split("?")[0].split("/")[0].split(":")[0].lower().split(".")[0]
    return dm


def generate_hash(magnet):
    xts = parse_qs(urlparse(magnet).query)["xt"]
    _, _, info_hash = xts[0].split(":")
    # _, info_hash = x.split(":")
    return info_hash.lower()


def generate_magnet(hash, name):
    url_encoded_name = quote_plus(name)
    magnet = (
        "magnet:?xt=urn:btih:"
        + hash
        + "&dn="
        + url_encoded_name
        + "&tr=http://track.one:1234/announce&tr=udp://track.two:80"
    )
    for tracker in AVAILABLE_TRACKERS:
        magnet += "&tr=" + tracker
    return magnet


from .yts import fetch_data_api as yts

AVAILABLE_HOSTS = [
    ("yts", yts),
]


def get_provider_handler(provider):
    for handler in AVAILABLE_HOSTS:
        if provider == handler[0]:
            return handler[1]
    return None
