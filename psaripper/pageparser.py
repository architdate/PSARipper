from bs4 import BeautifulSoup

from psaripper.metadata import EpisodeMetadata, ShowMetadata
from psaripper.PSAMedia import PSAMedia, PSAMode
from psaripper.util import get_media_type


def parse_page(url, scraper, mode):
    result = scraper.get(url)
    scrape = scrape_page(result, get_media_type(url), mode), ShowMetadata(result)
    if mode == PSAMode.Full or mode == PSAMode.Latest:
        return scrape
    elif mode == PSAMode.FHD:
        return [x for x in scrape[0] if EpisodeMetadata(x[0]).get_resolution() == 1080], scrape[1]
    elif mode == PSAMode.HD:
        return [x for x in scrape[0] if EpisodeMetadata(x[0]).get_resolution() == 720], scrape[1]


def scrape_page(result, mediatype, mode=PSAMode.Full):
    if mediatype == PSAMedia.TVShow:
        # TV show parsing
        c = result.content
        soup = BeautifulSoup(c, features="lxml")
        entries = soup.find_all("div", "entry-inner")
        if mode == PSAMode.Latest:
            all_entries = []
            end_of_list = False
            search_string = entries[0].hr.next_sibling
            while not end_of_list:
                if search_string.name == "hr":
                    end_of_list = True
                elif search_string != "\n":
                    all_entries.append(search_string)
                search_string = search_string.next_sibling
        elif mode == PSAMode.Full or mode == PSAMode.FHD or mode == PSAMode.HD:
            all_entries = entries[0].find_all("div", "sp-wrap sp-wrap-steelblue")
        else:  # undefined mode
            return None
        return [(entry.find_all('div')[0].getText().strip(), entry) for entry in all_entries]
    elif mediatype == PSAMedia.Movie:
        # Movie parsing
        c = result.content
        soup = BeautifulSoup(c, features="lxml")
        entries = soup.find_all("div", "entry-inner")
        titles = [i.parent.getText().strip() for i in entries[0].find_all('span', attrs={'style': 'color: #ff0000;'})]
        all_entries = entries[0].find_all("div", "sp-wrap sp-wrap-steelblue")
        valid = [entry for entry in all_entries if entry.div.getText().strip() == 'Download']
        return [(titles[i], valid[i]) for i in range(len(valid))]
    else:
        return None
