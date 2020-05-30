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
    info = qb.torrents_info()
    if not info:
        return torrents
    for torrent in info:
        torrents.append(torrent["hash"])
    return torrents


# check torrent progress
def check_if_torrent_complete(info_hash):
    torrent_list_completed = qb.torrents.info.completed()
    for torrent in torrent_list_completed:
        if torrent["hash"] == info_hash:
            return True
    return False


def get_torrent_progress(info_hash):
    progress = qb.torrents_files(hash=info_hash)[0]["progress"]
    print(progress)
    return progress


# get file path of video
def get_main_file_path(hash):
    VALID_FORMATS = ["mp4", "mkv", "avi", "mov"]
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
