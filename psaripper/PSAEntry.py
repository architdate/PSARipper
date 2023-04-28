from psaripper.metadata import EpisodeMetadata
from psaripper.util import create_scraper, decrypt_url


class PSAEntry:
    def __init__(self, entry, scraper):
        self.entry = entry
        self.scraper = scraper
        self.title = self.entry[0]
        self.torr_index = 1
        self.DEBUG = False

    def get_ddl_parts(self, entry):
        all_parts = self.entry[1].find_all('div', class_='dropshadowboxes-container')
        return [(part.a.text.strip(), part.a['href']) for part in all_parts if "Download" in part.a.text]

    def get_ddl_urls(self):
        parts = self.get_ddl_parts(self.entry)
        ddl_urls = {}
        for ddl in parts:
            try:
                ddlurl = decrypt_url(ddl[1], self.scraper)
                ddl_urls[ddl[0]] = ddlurl
            except Exception:
                if self.DEBUG:
                    print("[DEBUG] Cookie Flagged! Refreshing scraper")
                self.scraper = create_scraper()  # assign a new scraper, so new cookie??
                ddlurl = decrypt_url(ddl[1], self.scraper)
                ddl_urls[ddl[0]] = ddlurl
        return ddl_urls

    def get_torrent_urls(self):
        torrindex = self.entry[1].find_all('div')[self.torr_index].find_all('p')
        torrent = None
        for para in torrindex:
            if para.text.strip() == "TORRENT":
                torrent = para.strong.a['href']
        if not torrent:
            return []
        try:
            torrenturl = decrypt_url(torrent, self.scraper)
        except Exception:
            self.scraper = create_scraper()
            torrenturl = decrypt_url(torrent, self.scraper)
        return torrenturl

    def get_metadata(self):
        return EpisodeMetadata(self.title)
