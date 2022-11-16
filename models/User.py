from models.Video import Video
from models.Channel import Channel

class User:
    
    def __init__(self, videos: list[Video], channels: list[Channel]) -> None:
        self.videos = videos
        self.channels = channels