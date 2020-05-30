import requests
from bs4 import BeautifulSoup


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

    return data
