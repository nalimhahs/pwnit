import json
import requests
from bs4 import BeautifulSoup
from .utils import generate_magnet, generate_hash


def refine(s):  # for getting links below 1.5gb
    tag = s.split(" ")
    if tag[1] == "MB":
        return True
    return float(tag[0]) < 1.5


def fetch_data(url):
    site = requests.get(url)
    site_cont = BeautifulSoup(site.content, "html5lib")

    data = {}  # storing data

    # extracting contents
    img_url = site_cont.find("div", attrs={"id": "movie-poster"}).img["src"]
    description = site_cont.find("div", attrs={"id": "synopsis"}).p.text
    runtime = site_cont.find("span", attrs={"title": "Runtime"}).next_sibling
    infos = site_cont.find("div", attrs={"id": "movie-info"})
    name = infos.h1.text
    imdb_url = infos.find("a", attrs={"title": "IMDb Rating"})["href"]
    contents = site_cont.findAll("div", attrs={"class": "modal-torrent"})
    links = []
    # extracting sizes and quality
    for content in contents:
        quality = {}
        temp = content.findAll("p", attrs={"class": "quality-size"})
        if refine(temp[1].text):
            quality["size"], unit = temp[1].text.split(" ")
            if unit in ("GB", "gb"):
                quality["size"] = float(quality["size"]) * 1000
            else:
                quality["size"] = float(quality["size"])
            quality["quality"] = int(
                content.find("div", attrs={"class": "modal-quality"}).span.text.split(
                    "p"
                )[0]
            )
            quality["link"] = content.find("a", attrs={"class": "magnet-download"})[
                "href"
            ]
            links.append(quality)

    data["quality"] = links[0]["quality"]
    data["file_size"] = int(links[0]["size"])
    data["magnet_link"] = links[0]["link"]
    data["name"] = name
    data["imdb_url"] = imdb_url
    data["length"] = runtime
    data["description"] = description
    data["thumbnail"] = img_url
    data["provider"] = "yts"
    data["provider_id"] = url.split("/")[-1]
    data["magnet_hash"] = generate_hash(data["magnet_link"])

    return data


BASE_URL = "https://yts.mx/api/v2"


def movie_search_api(query):
    ENDPOINT = "/list_movies.json"
    result = requests.get(BASE_URL + ENDPOINT, params={"query_term": query})
    data = []
    for res in json.loads(result.text)["data"]["movies"]:
        mov = {
            "name": res["title_long"],
            "id": res["id"],
            # "quality": res["quality"],
            "provider": "yts",
        }
        data.append(mov)
    return data


def fetch_data_api(dat):
    id = dat["id"]
    ENDPOINT = "/movie_details.json"
    result = requests.get(BASE_URL + ENDPOINT, params={"movie_id": id})
    pre = json.loads(result.text)["data"]["movie"]
    data = {}
    for torrent in pre["torrents"]:
        if refine(torrent["size"]):
            data["quality"] = int(torrent["quality"].split("p")[0])
            size, unit = torrent["size"].split(" ")
            if unit in ("GB", "gb"):
                data["file_size"] = float(size) * 1000
            else:
                data["file_size"] = float(size)
            data["magnet_hash"] = torrent["hash"].lower()
            data["magnet_link"] = generate_magnet(
                data["magnet_hash"], pre["title_long"]
            )
            break
    data["name"] = pre["title_long"]
    data["imdb_url"] = "https://www.imdb.com/title/" + pre["imdb_code"] + "/"
    data["length"] = str(pre["runtime"])
    data["description"] = pre["description_full"]
    data["thumbnail"] = pre["medium_cover_image"]
    data["provider"] = "yts"
    data["provider_id"] = str(pre["id"])
    return data
