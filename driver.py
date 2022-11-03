from runTimeAPILoader import *
from offlineLoader import *
# myVideos = fetchAPIinfo('watch-history.html')
# file = open('videos.dictionary', 'wb')
# saveDictionaryFile(file, myVideos)

myVideos = loadAll('videos.dictionary')
for vid in myVideos:
    print(vid.channelName)