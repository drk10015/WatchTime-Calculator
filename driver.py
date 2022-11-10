from loads.runTimeAPILoader import *
from loads.offlineLoader import *
from views.MainWindowClass import MainWindow
from utils.commandline.commandTools import *
from PyQt6.QtWidgets import QApplication
import os, pathlib, sys
from utils.commandline.CompletionUtility import Completer
from views.LoadingWindow import LoadingWindow

CURRENT_DIRECTORY = pathlib.Path(__file__).parent.resolve()
CURRENT_FILES = os.listdir(CURRENT_DIRECTORY)
loadCompletion = Completer(['online load', 'offline pickle']).complete
channelCompletion = Completer(['search', 'channel watchtime']).complete
videoCompletion = Completer(['search', 'video watchtime']).complete
driverCompletion = Completer(['channels', 'videos']).complete
pathCompletion = Completer([]).pathCompleter
LOADED = False
usersVideos = []
if 'videos.dictionary' in CURRENT_FILES:
    try:
        print('Trying to offline load...')
        usersVideos = loadAll('videos.dictionary')
        LOADED = True
        print('Success. Able to load your "videos.dictionary" file.')
    except:
        print('Was unable to find default file, "videos.dictionary" in current directory...\nTrying online load...')
if not LOADED and 'watch-history.html' in CURRENT_FILES:
    # try: 
    print('Trying online load...This may take a few moments...')
    usersVideos = fetchAPIinfo('watch-history.html')
    LOADED = True
    print('Success loading online.')
    response = input('Save values as Dictionary for quicker loading times? y/n').lower()
    if response == 'y' or response == 'yes':
        saveDictionaryFile(usersVideos)
    # except:
    #     print('Error loading online, resorting to manual user load...')

app = QApplication(sys.argv)
window = LoadingWindow()
window.show()
app.exec()
