from models.Video import *
from bs4 import BeautifulSoup, SoupStrainer
import time
import requests
import pickle
#Change String from ISO (YouTube) format to Seconds (Int)
def fromISOtoSec(isoString) -> int:
    #Reserved for future use
    # daysPlus = isoString[:isoString.index('T')]
    #Get time numbers
    currentIndex = 0
    hours = 0
    minutes = 0
    seconds = 0
    previousIndex = 0
    totalTime = 0
    if 'T' in isoString:
        time = isoString[isoString.index('T') + 1 :]
        if 'H' in isoString:
            while time[currentIndex] != 'H':
                currentIndex += 1
            hours = int(time[:currentIndex]) * 3660
            previousIndex = currentIndex + 1
        if 'M' in isoString:
            while time[currentIndex] != 'M':
                currentIndex += 1
            minutes = int(time[previousIndex:currentIndex]) * 60
            previousIndex = currentIndex + 1
        if 'S' in isoString:
            while time[currentIndex] != 'S':
                currentIndex += 1
            seconds = int(time[previousIndex:currentIndex])
        totalTime = hours + minutes + seconds
    return totalTime

#Cut out the ID for the video from the Youtube URL
def getVidIDfromURL(urlStr) -> str:
        # print(urlStr)
        return urlStr[urlStr.index('=') + 1:]
#Cut out channel ID from the channel URL
def getChannelID(url) -> str:
    return url[url.index('channel/') + 8:]
#extracts date from youtube webpage html
def extractDate(str) -> str:
    arr=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    i = -27
    while i > -100:
        for month in arr:
            if month in str[i:]:
                return str[i:]
        i -= 1
#find object and attach date
def attachDateToObj(id, dict, date) -> None:
    
    for obj in dict:
        if obj.id == id:
            obj.date = date
#Creates a video object from the decoded json
def getVideofromJSON(file, json) -> Video:
    youtubeVidBase = "https://www.youtube.com/watch?v="
    youtubeChannelBase = "https://www.youtube.com/channel/"
    # try:
    items = json['items']
    ret = []
    for video in items:
        # print(video)
        thumbnail = ''
        try:
            thumbnail = video['snippet']['thumbnails']['maxres']['url']
        except:
            try:
                thumbnail = video['snippet']['thumbnails']['standard']['url']
            except:
                thumbnail = video['snippet']['thumbnails']['default']['url']
        ret.append(Video(youtubeVidBase + video['id'], 
            youtubeChannelBase + video['snippet']['channelId'],
            video['id'],
            fromISOtoSec(video['contentDetails']['duration']),
            video['snippet']['channelTitle'],
            video['snippet']['title'],
            video['snippet']['categoryId'], 
            thumbnail=thumbnail,
            description=video['snippet']['description']))
    return ret
    # except:
        # file.close()
        # print(json)
        # exit()
# fetches the channel, category name, and duration in one API call
# returns an array of Video objects
def fetchAPIinfo(fileName, window = None) -> list[Video] :
    print('SUCCESSSSS')
    print(fileName)
    if window:
        window.show()
        print(window)
    watchHistory = open(fileName, encoding="utf8")
    window.worker.signals.timeRemaining.emit('Utilizing BeautifulSoup\nThis may take a moment.')
    soup_strainer = SoupStrainer('div', attrs={'class':'content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1'})
    doc = BeautifulSoup(watchHistory, 'html.parser', on_duplicate_attribute='ignore' ,parse_only=soup_strainer)
    print('Out of Soup')
    ret = []
    ids = []
    dates = []
    window.worker.signals.timeRemaining.emit('Out of Soup. Indexing...')
    for div in doc('div'):
        active = len(div('a'))
        if active > 1:
            for a in div('a'):
                # if not (getVidIDfromURL(div('a')[0]['href']) in ids):
                if 'watch' in a['href'] and not (getVidIDfromURL(a['href']) in ids):
                    ids.append(getVidIDfromURL(a['href']))
                    dates.append(extractDate(div.getText()))
            
            # print(dates)
    base_api_url = 'https://www.googleapis.com/youtube/v3/videos?part=snippet&part=contentDetails'
    api_url = base_api_url
    beginning = time.perf_counter()
    totalTime = 0
    num = 1
    for i in range(0,len(ids)):
        api_url += '&id=' + ids[i]
        if (i % 49 == 0 and i != 0) or i == len(ids) - 1:
            api_url += '&key=AIzaSyDNHNVXw6TFETWGo8kdjAP4wvszh1ti-VQ'
            response = requests.get(api_url)
            obj = response.json()
            ret += getVideofromJSON(watchHistory, obj)
            end = time.perf_counter()
            elapsed_time = (end - beginning) / 60
            totalTime += elapsed_time
            averageTime = ((totalTime) / num)
            percentageLeft = (1 - (i / len(ids)) )
            if window:
                window.worker.signals.progress.emit(int((i / len(ids)) * 100))
                window.worker.signals.timeRemaining.emit('Estimated Time Remaining: ' + str(int((averageTime * ((percentageLeft * len(ids))/ 50)) * 60)) + ' seconds')
            # print('Estimated Time Remaining:', round((averageTime * ((percentageLeft * len(ids))/ 50)), 2) * 60, 'seconds')
            beginning = time.perf_counter()
            api_url = base_api_url
            num += 1
    for i in range(0, len(ret)):
        ret[i].dateWatched = dates[i]
    if window:
        window.worker.signals.result.emit(ret)
    else:
        return ret
#write dictionary; takes file handle and array of objects
def saveDictionaryFile(array):
    file = open('videos.dictionary', 'wb')
    for item in array:
        pickle.dump(item, file)
    file.close()