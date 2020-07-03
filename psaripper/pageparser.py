from psaripper.util import get_media_type
from psaripper.PSAMedia import PSAMedia, PSAMode
from bs4 import BeautifulSoup

def parse_page(url, scraper, mode):
    result = scraper.get(url)
    return scrape_page(result, get_media_type(url), mode)

def scrape_page(result, mediatype, mode = PSAMode.Full):
    if mediatype == PSAMedia.TVShow:
        # TV show parsing
        c = result.content
        soup = BeautifulSoup(c, features="lxml")
        entries = soup.find_all("div", "entry-inner")
        if mode == PSAMode.Latest:
            all_entries = []
            end_of_list = False
            search_string = entries[0].hr.next_sibling
            while end_of_list == False:
                if search_string.name == "hr":
                    end_of_list = True
                elif search_string != "\n":
                    all_entries.append(search_string)
                search_string = search_string.next_sibling
        elif mode == PSAMode.Full:
            all_entries = entries[0].find_all("div", "sp-wrap sp-wrap-steelblue")
        else: # undefined mode
            return None 
        return [(entry.find_all('div')[0].getText().strip(), entry) for entry in all_entries]
    elif mediatype == PSAMedia.Movie:
        # Movie parsing
        c = result.content
        soup = BeautifulSoup(c, features="lxml")
        entries = soup.find_all("div", "entry-inner")
        titles = [i.parent.getText().strip() for i in entries[0].find_all('span', attrs={'style':'color: #ff0000;'})]
        all_entries = entries[0].find_all("div", "sp-wrap sp-wrap-steelblue")
        valid = [entry for entry in all_entries if entry.div.getText().strip() == 'Download']
        return [(titles[i], valid[i]) for i in range(len(valid))]
    else:
        return None