import requests, bs4, json, uvicorn
from fastapi import FastAPI

app = FastAPI()

config = {}

def read_config() -> dict:
    with open("config.json", "r") as c:
        return json.loads(c.read())

# scrape nhentai.to
def get_from_code(code: int):
    r = requests.post(
        url=config['flaresolve_url'],
        json={
            "cmd": "request.get",
            "url":f"https://nhentai.net/api/gallery/{code}", # https://nhentai.net/api/gallery/177013
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
    
@app.get("/gallery/{code}")
def nhentai_by_code(code: int):
    return get_from_code(code)

    
if __name__ == '__main__':
    config = read_config()
    print(config)
    uvicorn.run(app, host=config['host'], port=config['port'])