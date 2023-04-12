import feedparser
from feedgen.feed import FeedGenerator

from psaripper.pageparser import parse_page
from psaripper.PSAEntry import PSAEntry
from psaripper.PSAMedia import PSAMode
from psaripper.util import create_scraper

PSA_FEED_URL = "https://psa.re/feed/"


def get_psa_feed(url=PSA_FEED_URL):
    return feedparser.parse(url)


def generate_feed(psa_feed):
    scraper = create_scraper()
    fg = FeedGenerator()
    fg.title("PSARipper Feed")
    fg.link(href=PSA_FEED_URL)
    fg.author({'name': 'Archit Date'})
    fg.subtitle('PSARips feed with bypassed shortner URLs for the latest entry')
    fg.language('en')
    for entry in psa_feed.entries:
        fe = fg.add_entry()
        fe.title = entry['title']
        try:
            latest, meta = parse_page(entry['link'], scraper, PSAMode.Latest)
            latest = latest[0]  # absolute latest
            media = PSAEntry(latest, scraper)
            fe.link(href=media.get_torrent_urls()[0])
        except Exception:
            fe.link(href=entry['link'])
        fe.description(media.title)
        fe.published(entry['published'])
        fe.author(name=entry['author'])
    rss = fg.rss_str(pretty=True)
    return rss
