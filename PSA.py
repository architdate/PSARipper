import cfscrape, sys
from psaripper.pageparser import parse_page
from psaripper.metadata import Hosters
from psaripper.PSAMedia import PSAMode
from psaripper.PSAEntry import PSAEntry

SCRAPER = cfscrape.create_scraper()

if __name__ == "__main__":
    MODE = PSAMode.Full

    if len(sys.argv) > 2:
        url = sys.argv[1]
        if sys.argv[2].lower() == "latest":
            MODE = PSAMode.Latest
        elif sys.argv[2].lower() == "1080p" or sys.argv[2].lower() == "fhd":
            MODE = PSAMode.FHD
        elif sys.argv[2].lower() == "720p" or sys.argv[2].lower() == "hd":
            MODE = PSAMode.HD
        else:
            MODE = PSAMode.Full

    elif len(sys.argv) > 1:
        url = sys.argv[1]

    else:
        url = input("Enter a PSA url - ")

    entries, metadata = parse_page(url, SCRAPER, MODE)
    if entries == None:
        print("Could not parse the page provided")
        sys.exit(-1)

    entries.reverse()
    print(f"Show: {metadata.get_show_title()}\nRating: {metadata.get_rating()}\n\n")
    for entry in entries:
        media = PSAEntry(entry, SCRAPER)
        metadata = media.get_metadata()
        ddlurls = media.get_ddl_urls()
        print(f"Title - {media.title}\nResolution - {metadata.get_resolution()}p\nChannels - {metadata.get_channel()} channels\nEncoding - x{metadata.get_encoding()}\n\nDDL - {ddlurls}\nTorrent - {media.get_torrent_urls()}\n\n")
