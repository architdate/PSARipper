import cfscrape, sys, os
from psaripper.pageparser import parse_page
from psaripper.metadata import Hosters
from psaripper.PSAMedia import PSAMode
from psaripper.PSAEntry import PSAEntry
from psaripper.rss import get_psa_feed, generate_feed
from psaripper.dump import get_hoster_dictionary, pretty_print, pretty_print_torr

SCRAPER = cfscrape.create_scraper()

def mode_parse(arg):
    arg = arg.strip().lower()
    if arg == "latest":
        return PSAMode.Latest
    elif arg == "1080p" or arg == "fhd":
        return PSAMode.FHD
    elif arg == "720p" or arg == "hd":
        return PSAMode.HD
    return PSAMode.Full

if __name__ == "__main__":
    MODE = PSAMode.Full

    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.makedirs('output', exist_ok=True)
    if '--rss' in sys.argv:
        feed = get_psa_feed()
        rss = generate_feed(feed)
        with open('output/rss.xml', 'wb') as f:
            f.write(rss)
        sys.exit(0)

    if len(sys.argv) > 2:
        url = sys.argv[1]
        MODE = mode_parse(sys.argv[2])

    elif len(sys.argv) > 1:
        url = sys.argv[1]

    else:
        url = input("Enter a PSA url - ")
        MODE = mode_parse(input("Enter download mode (latest/full/1080p/720p) - "))

    entries, metadata = parse_page(url, SCRAPER, MODE)
    if entries == None:
        print("Could not parse the page provided")
        sys.exit(-1)

    entries.reverse()
    showtitle = metadata.get_show_title()
    print(f"\nShow: {showtitle}\nRating: {metadata.get_rating()}\n")
    entry_json = {"Torrent": {}, "DDL": {}}
    for entry in entries:
        media = PSAEntry(entry, SCRAPER)
        title = media.title
        metadata = media.get_metadata()
        ddlurls = media.get_ddl_urls()
        torrurls = media.get_torrent_urls()
        entry_json["Torrent"][title] = torrurls
        entry_json["DDL"][title] = ddlurls
        
    with open(f'output/{showtitle}.log', 'w') as f:
        ddl_out = get_hoster_dictionary(entry_json["DDL"])
        f.write(pretty_print(ddl_out) + '\n\n' + pretty_print_torr(entry_json["Torrent"]))
        print(f"URLs saved here: {os.path.join(os.getcwd(), 'output', showtitle + '.log')}")