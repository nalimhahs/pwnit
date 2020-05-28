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
# for torrent in qb.torrents_info():
#     print(torrent)

# add torrent via magnet to download queue
def download_from_magnet(magnet):
    qb.torrents_add(urls=magnet)


# delete a torrent and the files associated
def delete_torrent(hashes):
    qb.torrents_delete(delete_files=True, hashes=hashes)


# get the progress of a particular torrent
def get_progress(hashes):
    return qb.torrents_info(hashes=hashes)


# get all running torrents
def get_all_torrent_hashes():
    torrents = []
    for torrent in qb.torrents_info():
        torrents.append(torrent.hash)
    return torrents


def check_if_torrent_complete(info_hash):
    torrent_list_completed = qb.torrents.info.completed()
    for torrent in torrent_list_completed:
        if torrent.info.hash == info_hash:
            return True
    return False


def get_main_file_path(hash):
    VALID_FORMATS = ["mp4", "mkv", "avi"]
    files = qb.torrents_files(hash=hash)
    valid = []
    for file in files:
        if file["name"][-3:] in VALID_FORMATS:
            valid.append(file)

    largest = valid[0]
    for video in valid:
        if video["size"] > largest["size"]:
            largest = video

    return qb.app.preferences["save_path"] + largest["name"]
