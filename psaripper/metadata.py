from enum import Enum


class EpisodeMetadata:
    def __init__(self, title):
        self.title = title

    def get_resolution(self):
        if "720p" in self.title:
            return 720
        elif "1080p" in self.title:
            return 1080
        else:
            return -1

    def get_channel(self):
        if "6CH" in self.title:
            return 6
        elif "2CH" in self.title:
            return 2
        else:
            return -1

    def get_encoding(self):
        if "HEVC" in self.title or "x265" in self.title:
            return 265
        return 264


class ShowMetadata:
    def __init__(self, results):
        self.text = results.text

    def get_show_title(self):
        return self.text.split('post-title entry-title">')[1].split('<')[0]

    def get_rating(self):
        try:
            return float(self.text.split("wpdrv'>")[1].split('<')[0])
        except Exception:
            return -1


class Hosters(Enum):
    PSARips = "download.psarips.net"
    UpToBox = "uptobox.com"
    Mega = "mega.nz"
    KatFile = "katfile.com"
    ClicknUpload = "clicknupload.co"
    NitroFlare = "nitroflare.com"
    Earn4Files = "earn4files.com"
    DropAPK = "dropapk.to"
    Uploader = "uploader.link"
    MegaUp = "megaup.net"
    DDownload = "ddownload.com"
    BayFiles = "bayfiles.com"
    AnonFiles = "anonfiles.com"
    SpeedDown = "speed-down.org"
    Unknown = "zyzzyspoonshift1"  # :P

    @classmethod
    def getHoster(cls, url):
        for hoster in cls:
            if hoster.value in url:
                return hoster
        return cls.Unknown
