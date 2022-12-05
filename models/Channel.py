from models.Video import Video

class Channel:

    def __init__(self, channelUrl: str, vids: list[Video], thumbnail: str, channelTitle: str, channelDescription: str, subscribers: int = None) -> None:
        self.id = self.getChannelID(channelUrl)
        self.channelVids = vids
        self.channelUrl = channelUrl
        self.timeWatched = self.getDuration()
        self.thumbnail = thumbnail
        self.channelTitle = channelTitle
        self.description = channelDescription

    def addTime(self, num: int) -> None:
        self.timeWatched += num

    def getDuration(self) -> int:
        ret = 0
        for vid in self.channelVids:
            ret += vid.duration
        return ret

    def getChannelID(self, url: str) -> str:
        return url[url.index('channel/') + 8:]
    
    def getRecentVideos(self, numOfVids = 1):
        ret = []
        self.channelVids = sorted(self.channelVids, key=lambda vid: vid.getDateCode(), reverse=True)
        if len(self.channelVids) > 0:
            for i in range(0, numOfVids):
                ret.append(self.channelVids[i])
        else:
            return [0]
        return ret