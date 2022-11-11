from Video import Video

class Channel():
    
    def __init__(self, channelUrl: str, vids: list(Video), duration: int, thumbnail: str) -> None:
        self.id = id
        self.channelVids = vids
        self.channelUrl = channelUrl
        self.timeWatched = duration
        self.thumbnail = thumbnail