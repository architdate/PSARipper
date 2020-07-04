import requests, time, base64, cfscrape
from bs4 import BeautifulSoup
from psaripper.PSAMedia import PSAMedia

def get_headers():
    # Creating headers
    headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9" -H "sec-fetch-site: none" -H "sec-fetch-mode: navigate',
               'accept-language': 'en-GB,en;q=0.8,en-US;q=0.6,ml;q=0.4',
               'sec-fetch-dest': 'document',
               'upgrade-insecure-requests': '1',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
               'authority': 'get-to.link',
               'sec-fetch-site': 'none',
               'sec-fetch-mode': 'navigate',
               'sec-fetch-user': '?1'}
    return headers

def get_urls(url):
    try:
        res = requests.get(url, headers=get_headers())
        c = res.content
        if "Your access to this site has been limited" in res.text:
            print("Rate Limit ban detected. Waiting 60 seconds + 5 buffer seconds to bypass ...\n")
            time.sleep(65)
            res = requests.get(url, headers=get_headers())
            c = res.content
        soup = BeautifulSoup(c, "lxml")
        entry = soup.find_all("div", "entry-content")[0]
        links = entry.find_all('a')
        return [x.get('href') for x in links]
    except:
        # Legacy URLs with spaste, cannot bypass
        return [url]

def decrypt_url(url, scraper):
    urlt = "must-revalidate"
    while "must-revalidate" in urlt:
        urlr = scraper.get(url, allow_redirects=False, headers=get_headers())
        urlt = urlr.text
    furl = base64.b64decode(urlt.split("url\' value=")[1].split('/>')[0].strip()).decode('utf-8')
    return get_urls(furl)

def get_media_type(url):
    if "tv-show" in url:
        return PSAMedia.TVShow
    return PSAMedia.Movie