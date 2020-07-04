import base64, cfscrape
from psaripper.util import decrypt_url
from psaripper.metadata import EpisodeMetadata

class PSAEntry:
    def __init__(self, entry, scraper):
        self.entry = entry
        self.scraper = scraper
        self.title = self.entry[0]
        self.torr_index = 1
        self.DEBUG = False

    def get_ddl_parts(self, entry):
        all_parts = self.entry[1].find_all('div', class_='dropshadowboxes-container')
        return [(part.a.text.strip(), f"https://psarips.xyz{part.a['href']}") for part in all_parts if "Download" in part.a.text]

    def get_ddl_urls(self):
        parts = self.get_ddl_parts(self.entry)
        ddl_urls = {}
        for ddl in parts:
            try:
                ddlurl = decrypt_url(ddl[1], self.scraper)
                ddl_urls[ddl[0]] = ddlurl
            except:
                if self.DEBUG:
                    print("[DEBUG] Cookie Flagged! Refreshing scraper")
                self.scraper = cfscrape.create_scraper() # assign a new scraper, so new cookie??
                ddlurl = decrypt_url(ddl[1], self.scraper)
                ddl_urls[ddl[0]] = ddlurl
        return ddl_urls

    def get_torrent_urls(self):
        torrindex = self.entry[1].find_all('div')[self.torr_index].find_all('p')
        torrent = None
        for para in torrindex:
            if para.text.strip() == "TORRENT":
                torrent = f"https://psarips.xyz{para.strong.a['href']}"
        if torrent == None:
            return []
        try:
            torrenturl = decrypt_url(torrent, self.scraper)
        except:
            self.scraper = cfscrape.create_scraper()
            torrenturl = decrypt_url(torrent, self.scraper)
        return torrenturl

    def get_metadata(self):
        return EpisodeMetadata(self.title)