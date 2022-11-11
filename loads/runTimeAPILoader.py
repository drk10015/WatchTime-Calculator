import pickle
import time

import requests, traceback
from bs4 import BeautifulSoup, SoupStrainer

from models.Video import *

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
def getVideofromJSON(file, vjson) -> Video:
    youtubeVidBase = "https://www.youtube.com/watch?v="
    youtubeChannelBase = "https://www.youtube.com/channel/"
    try:
        vitems = vjson['items']
        # citems = cjson['items']
        ret = []
        for i in range(0, len(vitems)):
            vthumbnail = ''
            # cthumbnail = ''
            # try:
            #     cthumbnail = citems[i]['snippet']['thumbnails']['high']
            # except:
            #     try:
            #         cthumbnail = citems[i]['snippet']['thumbnails']['medium']
            #     except:
            #         cthumbnail = citems[i]['snippet']['thumbnails']['default']
            try:
                vthumbnail = vitems[i]['snippet']['thumbnails']['maxres']['url']
            except:
                try:
                    vthumbnail = vitems[i]['snippet']['thumbnails']['standard']['url']
                except:
                    vthumbnail = vitems[i]['snippet']['thumbnails']['default']['url']
            ret.append(Video(youtubeVidBase + vitems[i]['id'], 
                youtubeChannelBase + vitems[i]['snippet']['channelId'],
                vitems[i]['id'],
                fromISOtoSec(vitems[i]['contentDetails']['duration']),
                vitems[i]['snippet']['channelTitle'],
                vitems[i]['snippet']['title'],
                vitems[i]['snippet']['categoryId'], 
                thumbnail=vthumbnail,
                description=vitems[i]['snippet']['description']))
        return ret
    except:
        file.close()
        print(vjson)
        # traceback.print_exception()
        exit()
# fetches the channel, category name, and duration in one API call
# returns an array of Video objects
def fetchAPIinfo(fileName, window = None) -> list[Video] :
    if window:
        window.show()
    watchHistory = open(fileName, encoding="utf8")
    window.worker.signals.timeRemaining.emit('Utilizing BeautifulSoup\nThis may take a moment.')
    soup_strainer = SoupStrainer('div', attrs={'class':'content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1'})
    doc = BeautifulSoup(watchHistory, 'html.parser', on_duplicate_attribute='ignore' ,parse_only=soup_strainer)
    print('Out of Soup')
    ret = []
    vidIds = []
    channelIds = []
    dates = []
    window.worker.signals.timeRemaining.emit('Out of Soup. Indexing...')
    for div in doc('div'):
        active = len(div('a'))
        if active > 1:
            for a in div('a'):
                # if not (getVidIDfromURL(div('a')[0]['href']) in ids):
                if 'watch' in a['href'] and not (getVidIDfromURL(a['href']) in vidIds):
                    vidIds.append(getVidIDfromURL(a['href']))
                    channelIds.append(getChannelID(div('a')[1]['href']))
                    dates.append(extractDate(div.getText()))
            # print(dates)
    video_base_api_url = 'https://www.googleapis.com/youtube/v3/videos?part=snippet&part=contentDetails'
    channel_base_api_url = 'https://www.googleapis.com/youtube/v3/channels?part=snippet'
    video_api_url = video_base_api_url
    channel_api_url = channel_base_api_url
    beginning = time.perf_counter()
    totalTime = 0
    num = 1
    print(vidIds)
    for i in range(0,len(vidIds)):
        video_api_url += '&id=' + vidIds[i]
        channel_api_url += '&id=' + channelIds[i]
        if (i % 49 == 0 and i != 0) or i == len(vidIds) - 1:
            video_api_url += '&key=AIzaSyDNHNVXw6TFETWGo8kdjAP4wvszh1ti-VQ'
            channel_api_url += '&key=AIzaSyDNHNVXw6TFETWGo8kdjAP4wvszh1ti-VQ'
            print(video_api_url)
            response = requests.get(video_api_url)
            vidobj = response.json()
            chanobj = requests.get(channel_api_url)
            chanobj = response.json()
            ret += getVideofromJSON(watchHistory, vidobj)
            end = time.perf_counter()
            elapsed_time = (end - beginning) / 60
            totalTime += elapsed_time
            averageTime = ((totalTime) / num)
            percentageLeft = (1 - (i / len(vidIds)) )
            if window:
                window.worker.signals.progress.emit(int((i / len(vidIds)) * 100))
                window.worker.signals.timeRemaining.emit('Estimated Time Remaining: ' + str(int((averageTime * ((percentageLeft * len(vidIds))/ 50)) * 60)) + ' seconds')
            # print('Estimated Time Remaining:', round((averageTime * ((percentageLeft * len(ids))/ 50)), 2) * 60, 'seconds')
            beginning = time.perf_counter()
            video_api_url = video_base_api_url
            channel_api_url = channel_base_api_url
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