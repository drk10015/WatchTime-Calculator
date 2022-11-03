class Video:
    def __init__(self, videoURL: str, channelURL: str, id: str = None, duration: int = None, channelName: str = None, category: str = None, date: str = None) -> None:
        # self.title = title
        self.id = id
        self.videoURL = videoURL
        self.channelURL = channelURL
        self.duration = duration
        self.channelName = channelName
        self.category = category
        self.dateWatched = date
    
    def getCategoryName(self):
        categoryMap = {'1':'Film & Animation','2':'Autos & Vehicles','10': 'Music','15':'Pets & Animals','17': 'Sports','18': 'Short Movies','19': 'Travel & Events','20': 'Gaming','21': 'Videoblogging','22': 'People & Blogs','23': 'Comedy','24': 'Entertainment','25': 'News & Politics','26': 'Howto & Style', '27': 'Education', '28': 'Science & Technology', '29': 'Nonprofits & Activism','30': 'Movies','31': 'Anime/Animation','32': 'Action/Adventure','33': 'Classics','34': 'Comedy','35': 'Documentary', '36': 'Drama', '37': 'Family','38': 'Foreign', '39': 'Horror', '40': 'Sci-Fi/Fantasy','41': 'Thriller', '42': 'Shorts', '43': 'Shows', '44': 'Trailers'}
        return categoryMap[self.category]