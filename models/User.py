from models.Video import Video
from models.Channel import Channel

class User:
    
    def __init__(self, videos: list[Video], channels: list[Channel]) -> None:
        self.videos = videos
        self.channels = channels
        
    def getChannelFromId(self, id):
        for channel in self.channels:
            if id == channel.id:
                return channel