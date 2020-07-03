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

    entries, metadata = parse_page(url, SCRAPER, MODE)
    if entries == None:
        print("Could not parse the page provided")
        sys.exit(-1)

    entries.reverse()
    print(f"Show: {metadata.get_show_title()}\nRating: {metadata.get_rating()}\n\n")
    for entry in entries:
        media = PSAEntry(entry, SCRAPER)
        metadata = media.get_metadata()
        print(f"Title - {media.title}\nResolution - {metadata.get_resolution()}p\nChannels - {metadata.get_channel()} channels\nEncoding - x{metadata.get_encoding()}\n\nDDL - {media.get_ddl_urls()}\nTorrent - {media.get_torrent_urls()}\n\n")