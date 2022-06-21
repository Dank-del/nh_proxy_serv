import requests
import bs4
import json
import uvicorn
from utils import app, get_from_code, get_from_search, read_config


@app.get("/gallery/{code}")
def nhentai_by_code(code: int):
    return get_from_code(code)


@app.get("/galleries/search")
def nhentai_by_search(query: str, page: int = 1, sort: str = 'recent', language: str = 'english'):
    return get_from_search(query, page, language, sort)


@app.get("/galleries/all")
def all_nhentai(page: int = 1):
    r = requests.post(
        url=config['flaresolve_url'],
        json={
            "cmd": "request.get",
            # https://nhentai.net/api/gallery/177013
            "url": f"https://nhentai.net/api/galleries/all?page={page}",
            "maxTimeout": 60000
        }
    )
    soup = bs4.BeautifulSoup(r.json()['solution']['response'], "lxml")
    return json.loads(soup.find('body').find('pre').text)


if __name__ == '__main__':
    config = read_config()
    # print(config)
    uvicorn.run(app, host=config['host'], port=config['port'])
    #print(get_from_search("big breasts"))
