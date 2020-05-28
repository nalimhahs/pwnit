import qbittorrentapi

# instantiate a Client using the appropriate WebUI configuration
qb = qbittorrentapi.Client(
    host="localhost:8080",
    username="admin",
    password="adminadmin",
    SIMPLE_RESPONSES=True,
)

try:
    qb.auth_log_in()
except qbittorrentapi.LoginFailed as e:
    print(e)

# retrieve and show all torrents
for torrent in qb.torrents_info():
    print(f"{torrent.hash[-6:]}: {torrent.name} ({torrent.state})")


def download_magnet(magnet):
    qb.torrents_add(urls=magnet)


def delete_torrent(hashes):
    qb.torrents_delete(delete_files=True, hashes=hashes)


def get_progress(hashes):
    qb.torrents_info(hashes=hashes)
