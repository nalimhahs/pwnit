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

# add torrent via magnet to download queue
def download_from_magnet(magnet):
    qb.torrents_add(urls=magnet)


# delete a torrent and the files associated
def delete_torrent(hashes):
    qb.torrents_delete(delete_files=True, hashes=hashes)


# get the progress of a particular torrent
def get_progress(hashes):
    qb.torrents_info(hashes=hashes)


# get all running torrents
def get_all_torrent_hashes():
    torrents = []
    for torrent in qb.torrents_info():
        torrents.append(torrent.hash)
    return torrents


def check_if_torrent_complete(hash):
    torrent_list_completed = qb.torrents.info.completed()
    for torrent in torrent_list_completed:
        if torrent.info.hash == hash:
            return True
    return False
