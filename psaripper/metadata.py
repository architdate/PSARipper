
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
        except:
            return -1