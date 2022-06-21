import json
import urllib
import bs4
from fastapi import FastAPI
import requests


def build_url(base_url, path, args_dict):
    '''
    Returns a list in the structure of urlparse.ParseResult
    '''
    url_parts = list(urllib.parse.urlparse(base_url))
    url_parts[2] = path
    url_parts[4] = urllib.parse.urlencode(args_dict)
    return urllib.parse.urlunparse(url_parts)


config = {}
app = FastAPI(title="Sayan's nhentai API")

def read_config() -> dict:
    with open("config.json", "r") as c:
        return json.loads(c.read())


def get_from_search(query: str, page: int = 1, language: str = 'english', sort: str = 'recent'):
    r = requests.post(
        url=config['flaresolve_url'],
        json={
            "cmd": "request.get",
            "url": build_url('https://nhentai.net/', '/api/galleries/search', {
                'query': query,
                'page': page,
                'language': language,
                'sort': sort
            }),  # https://nhentai.net/api/gallery/177013
            "maxTimeout": 60000
        }
    )
    # print(r.json()['solution']['response'])
    # return
    soup = bs4.BeautifulSoup(r.json()['solution']['response'], "lxml")
    return json.loads(str(soup.find('body').find('pre').text))


def get_from_code(code: int):
    r = requests.post(
        url=config['flaresolve_url'],
        json={
            "cmd": "request.get",
            # https://nhentai.net/api/gallery/177013
            "url": f"https://nhentai.net/api/gallery/{code}",
            "maxTimeout": 60000
        }
    )
    # print(r.json()['solution']['response'])
    # return
    soup = bs4.BeautifulSoup(r.json()['solution']['response'], "lxml")
    '''
    for x in soup.findAll(text=lambda text:isinstance(text, bs4.Comment)):
        x = bs4.element.Comment(x)
        if x.find('N.gallery') != -1:
            js = x.removeprefix('<script type="text/javascript">').removesuffix('</script>')
            # json_text = js.split("N.gallery(", 1)[1].split(")", 1)[0]

            print(js)
    '''
    return json.loads(soup.find('body').find('pre').text)
