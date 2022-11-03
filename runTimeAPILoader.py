import datetime as dt
from Video import *
from bs4 import BeautifulSoup, SoupStrainer
import time
import pickle
import keys
import requests
#Change String from ISO (YouTube) format to Seconds (Int)
def fromISOtoSec(isoString):
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
#Shift global Keysto a new one that will hopefully work
def shiftKeys():
    keys.CURRENT_INDEX =  (keys.CURRENT_INDEX + 1) % 12
    keys.CURRENT_KEY =  keys.API_KEYS[keys.CURRENT_INDEX]
    if keys.CURRENT_INDEX == 0:
        exit()
#Cut out the ID for the video from the Youtube URL
def getVidIDfromURL(urlStr):
        print(urlStr)
        return urlStr[urlStr.index('=') + 1:]
#Cut out channel ID from the channel URL
def getChannelID(url):
    return url[url.index('channel/') + 8:]





def fetchDuration(id):
    global config_dictionary
    api_url = 'https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id=' + id + '&key=' + keys.CURRENT_KEY
    response = requests.get(api_url)
    try:
        return response.json()['items'][0]['contentDetails']['duration']
    except:
        if response.json()['error']['code']:
            # touchBase(response.json(), dt.datetime.now())
            shiftKeys()
        print(response.json())



if __name__ == '__main__':
    watchHistory = open('watch-history.html', encoding="utf8")
    soup_strainer = SoupStrainer('div', attrs={'class':'content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1'})
    doc = BeautifulSoup(watchHistory, 'html.parser', on_duplicate_attribute='ignore' ,parse_only=soup_strainer)
    channelLinks = []
    videoLinks = []
    videos = []
    inactiveLinks = 0
    i = 0
    beginning = time.perf_counter()
    totalTimeWatched = 15515418
    config_dictionary = open('config.dictionary', 'ab')
    start = False
    print(str(len(doc('div'))))
    for div in doc('div'):
        if start:
            active = len(div('a'))
            if active > 1:
                for a in div('a'):
                    if 'channel' in a['href']:
                        channelLinks.append(a['href'])
                    # elif a['href'] in videoLinks:
                    #     break
                    else:
                        videoLinks.append(a['href'])
                id = getVidIDfromURL(videoLinks[i])
                duration = fromISOtoSec(fetchDuration(id))
                clear = True
                for video in videos:
                    if id == video.id:
                        clear = False
                        break
                if clear:
                    totalTimeWatched += duration
                    video = Video(videoLinks[i], channelLinks[i], id,duration)
                    videos.append(video)
                    pickle.dump(video, config_dictionary)
                    print(totalTimeWatched)
                i += 1
            else:
                inactiveLinks += 1
        else:
            for a in div('a'):
                if 'mpjREfvZiDs' in a['href']:
                    start = True
    end = time.perf_counter()
    config_dictionary.close()

#
def fetchChannelAnndCategoryName(id):
    global file
    api_url = 'https://www.googleapis.com/youtube/v3/videos?part=snippet&id=' + id + '&key=AIzaSyAIAyNLdUumVrXStTs8IjZGcVh7xSYD2_8'
    response = requests.get(api_url)
    obj = response.json()
    try:
        return {'Channel' : obj['items'][0]['snippet']['channelTitle'],
                'Category': obj['items'][0]['snippet']['categoryId']}
    except:
        if response.json()['error']['code']:
            # touchBase(response.json(), dt.datetime.now())
            shiftKeys()
        print(response.json())

def fetchCategoryName(id):
    global file
    api_url = 'https://www.googleapis.com/youtube/v3/videos?part=snippet&id=' + id + '&key=AIzaSyDwv7uJfRm7TEiMiAE0XgeQ1YIoYIj2lwA'
    response = requests.get(api_url)
    try:
        return response.json()['items'][0]['snippet']['categoryId']
    except:
        # if response.json()['error']['code']:
        #     touchBase(response.json(), dt.datetime.now())
        print(response.json())
        file.close()
        exit()
def apiCategoryDriver():
    w2 = dictionarymaker.loadAll('channel.dictionary')
    totalLen = len(w2)
    file = open('video.dictionary', 'ab')
    i = 0
    beginning = dt.perf_counter()
    end = 0
    t = False
    elapsed = 0
    prediction = 0
    average = 0
    total = 0
    offset = 0
    for video in w2:
        id = getVidIDfromURL(video.videoURL)
        category = fetchCategoryName(id)
        video.category = category
        pickle.dump(video, file)
        
        if i % 150 == 0 and i != 0:
            total = 0
            average = 0
            offset += 1
        i += 1
        percentage = (i/totalLen) * 100
        end = dt.perf_counter()
        elapsed = (end - beginning)
        prediction = (elapsed * (totalLen - i)) / 60
        total += prediction
        average = total / (i - (150 * offset))
        beginning = dt.perf_counter()
        print(str(average), 'minutes\n', str(elapsed))
        print(str(percentage) + '%')