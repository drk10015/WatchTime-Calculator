import datetime as dt
class Video:
    def __init__(self, videoURL: str, channelURL: str, id: str = None, duration: int = None, channelName: str = None, videoName: str = None, category: str = None, date: str = None, thumbnail: str = None, description: str = None,channelThumbnail:str = None) -> None:
        # self.title = title
        self.id = id
        self.videoURL = videoURL
        self.channelURL = channelURL
        self.duration = duration
        self.channelName = channelName
        self.videoName = videoName
        self.category = category
        self.dateWatched = date
        self.thumbnail = thumbnail
        self.description = description
        self.channelID = self.getChannelID(channelURL)
        self.channelThumbnail = channelThumbnail
    
    def getCategoryName(self):
        categoryMap = {'1':'Film & Animation','2':'Autos & Vehicles','10': 'Music','15':'Pets & Animals','17': 'Sports','18': 'Short Movies','19': 'Travel & Events','20': 'Gaming','21': 'Videoblogging','22': 'People & Blogs','23': 'Comedy','24': 'Entertainment','25': 'News & Politics','26': 'Howto & Style', '27': 'Education', '28': 'Science & Technology', '29': 'Nonprofits & Activism','30': 'Movies','31': 'Anime/Animation','32': 'Action/Adventure','33': 'Classics','34': 'Comedy','35': 'Documentary', '36': 'Drama', '37': 'Family','38': 'Foreign', '39': 'Horror', '40': 'Sci-Fi/Fantasy','41': 'Thriller', '42': 'Shorts', '43': 'Shows', '44': 'Trailers'}
        return categoryMap[self.category]

    def getChannelID(self, url) -> str:
        return url[url.index('channel/') + 8:]
    
    def getDateCode(self)-> dt.datetime:
        date = self.dateWatched.split(' ')
        arr=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        month = day = year = hour = minute = second = 0
        for m in arr:
            if date[0] == m:
                month = arr.index(m) + 1
        day = int(date[1][:-1])
        year = int(date[2][:-1])
        time = date[3].split(':')
        hour = int(time[0])
        if date[4] == 'PM':
            hour += 12
        minute = int(time[1])
        second = int(time[2])
        datetime_object = dt.datetime(year, month, day, hour - 1, minute, second)
        epoch = dt.datetime(1970,1,1)
        delta = (datetime_object - epoch)
        return delta.total_seconds()
        
