import requests
from bs4 import BeautifulSoup


def refine(s):  # for getting links below 1.5gb
    tag = s.split(" ")
    if tag[1] == "MB":
        return True
    return float(tag[0]) < 1.5


async def fetch_data(url):
    site = await requests.get(url)
    site_cont = BeautifulSoup(site.content, "html5lib")

    data = {}  # storing data

    # extracting contents
    img_url = site_cont.find("div", attrs={"id": "movie-poster"}).img["src"]
    description = site_cont.find("div", attrs={"id": "synopsis"}).p.text
    runtime = site_cont.find("span", attrs={"title": "Runtime"}).next_sibling
    infos = site_cont.find("div", attrs={"id": "movie-info"})
    name = infos.h1.text
    imbd_url = infos.find("a", attrs={"title": "IMDb Rating"})["href"]
    contents = site_cont.findAll("div", attrs={"class": "modal-torrent"})

    # extracting sizes and quality
    for content in contents:
        quality = {}
        temp = content.findAll("p", attrs={"class": "quality-size"})
        if refine(temp[1].text):
            quality["size"] = temp[1].text
            quality["quality"] = content.find(
                "div", attrs={"class": "modal-quality"}
            ).span.text
            quality["links"] = content.find("a", attrs={"class": "magnet-download"})[
                "href"
            ]
            data[quality["quality"] + "-" + temp[1].text] = quality

    data["name"] = name
    data["imbd_url"] = imbd_url
    data["length"] = runtime
    data["contents"] = description
    data["thumbnail"] = img_url

    return data
