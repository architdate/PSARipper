import base64
import re
from datetime import datetime
from urllib.parse import urlparse

import cfscrape
import requests
from bs4 import BeautifulSoup

from psaripper.PSAMedia import PSAMedia


def create_scraper(**kwargs):
    today = datetime.today().strftime("%Y%m%d")
    today_2 = base64.b64encode(datetime.today().strftime("%d%m%y").encode()).decode()
    headers = {
        "Cookie": f"clks={today}; ez4s={int(today)+1}; LstVstD={today_2}; shrnkio={today}; try2={today}; VstCnt=NQ%3D%3D;",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    }
    headers.update(kwargs)
    scraper = cfscrape.create_scraper(headers=headers)
    return scraper


def get_urls(url):
    scraper = create_scraper(referer=url)
    try:
        res = scraper.get(url)
        c = res.content
        soup = BeautifulSoup(c, "lxml")
        entry = soup.find_all("div", "entry-content")[0]
        links = entry.find_all('a')
        return [x.get('href') for x in links]
    except Exception:
        return [url]


def decrypt_url(url, scraper: cfscrape.CloudflareScraper):
    urlr = scraper.get(url)
    soup = BeautifulSoup(urlr.content, "html.parser")
    ouo_url = soup.find("form")['action']
    furl = bypass_ouo(ouo_url)
    return get_urls(furl)


def get_media_type(url):
    if "tv-show" in url:
        return PSAMedia.TVShow
    return PSAMedia.Movie


def bypass_ouo(url: str) -> str:

    ANCHOR_URL = 'https://www.google.com/recaptcha/api2/anchor?ar=1&k=6Lcr1ncUAAAAAH3cghg6cOTPGARa8adOf-y9zv2x&co=aHR0cHM6Ly9vdW8uaW86NDQz&hl=en&v=1B_yv3CBEV10KtI2HJ6eEXhJ&size=invisible&cb=4xnsug1vufyr'

    def RecaptchaV3(ANCHOR_URL):
        url_base = 'https://www.google.com/recaptcha/'
        post_data = "v={}&reason=q&c={}&k={}&co={}"
        client = requests.Session()
        client.headers.update({
            'content-type': 'application/x-www-form-urlencoded'
        })
        matches = re.findall(r'([api2|enterprise]+)\/anchor\?(.*)', ANCHOR_URL)[0]
        url_base += matches[0] + '/'
        params = matches[1]
        res = client.get(url_base + 'anchor', params=params)
        token = re.findall(r'"recaptcha-token" value="(.*?)"', res.text)[0]
        params = dict(pair.split('=') for pair in params.split('&'))
        post_data = post_data.format(params["v"], token, params["k"], params["co"])
        res = client.post(url_base + 'reload', params=f'k={params["k"]}', data=post_data)
        answer = re.findall(r'"rresp","(.*?)"', res.text)[0]
        return answer

    client = requests.Session()
    tempurl = url.replace("ouo.press", "ouo.io")
    p = urlparse(tempurl)
    id = tempurl.split('/')[-1]

    res = client.get(tempurl)
    next_url = f"{p.scheme}://{p.hostname}/go/{id}"

    for _ in range(2):

        if res.headers.get('Location'):
            break

        bs4 = BeautifulSoup(res.content, 'lxml')
        inputs = bs4.form.findAll("input", {"name": re.compile(r"token$")})
        data = {input.get('name'): input.get('value') for input in inputs}

        ans = RecaptchaV3(ANCHOR_URL)
        data['x-token'] = ans

        h = {
            'content-type': 'application/x-www-form-urlencoded'
        }

        res = client.post(next_url, data=data, headers=h, allow_redirects=False)
        next_url = f"{p.scheme}://{p.hostname}/xreallcygo/{id}"

    return res.headers.get('Location')
