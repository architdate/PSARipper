import cfscrape, sys
from psaripper.pageparser import parse_page
from psaripper.PSAMedia import PSAMode
from psaripper.PSAEntry import PSAEntry

SCRAPER = cfscrape.create_scraper()

if __name__ == "__main__":
    MODE = PSAMode.Full

    if len(sys.argv) > 2:
        if sys.argv[2].lower() == "latest":
            MODE = PSAMode.Latest
        else:
            MODE = PSAMode.Full

    elif len(sys.argv) > 1:
        url = sys.argv[1]

    else:
        url = input("Enter a PSA url - ")

    entries = parse_page(url, SCRAPER, MODE)
    entries.reverse()
    
    for entry in entries:
        media = PSAEntry(entry, SCRAPER)
        print(f"Title - {media.title}\n\nDDL - {media.get_ddl_urls()}\nTorrent - {media.get_torrent_urls()}\n\n")