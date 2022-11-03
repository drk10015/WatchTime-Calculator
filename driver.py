from datetime import datetime
from Video import *
from runTimeAPILoader import getVidIDfromURL, fromISOtoSec, getChannelID
from bs4 import BeautifulSoup, SoupStrainer
import dictionarymaker
import pickle
import datetime 
from dateutil import parser
import time as dt
def attachDateToObj(id, dict, date):
    
    for obj in dict:
        if obj.id == id:
            obj.date = date
def extractDate(str):
    arr=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    i = -27
    while i > -100:
        for month in arr:
            if month in str[i:]:
                return str[i:]
        i -= 1
dict_path = 'video.dictionary'
# watchHistory = open('watch-history.html', encoding="utf8")
# soup_strainer = SoupStrainer('div', attrs={'class':'content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1'})
# doc = BeautifulSoup(watchHistory, 'html.parser', on_duplicate_attribute='ignore' ,parse_only=soup_strainer)
oldDict = dictionarymaker.loadAll(dict_path)
# vidDict = open('video.dictionary', 'wb')

# for div in doc('div'):
#     active = len(div('a'))
#     if active > 1:
#         for a in div('a'):
#             if 'watch' in a['href']:
#                 vidID = getIDfromURL(a['href'])
#                 attachDateToObj(vidID, oldDict, extractDate(div.getText()))
duration = 0
for item in oldDict:
    # pickle.dump(item, vidDict)
    if item.getCategoryName() == 'Comedy':
        duration += item.duration
print(datetime.timedelta(seconds =duration))