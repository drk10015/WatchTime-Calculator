import os, pathlib, sys

from PyQt6.QtWidgets import QApplication

from loads.offlineLoader import *
from loads.runTimeAPILoader import *
from utils.commandline.commandTools import *
from views.LoadingWindow import LoadingWindow
from views.MainWindowClass import MainWindow
from views.ProgressWindow import ProgressWindow

CURRENT_DIRECTORY = pathlib.Path(__file__).parent.resolve()
CURRENT_FILES = os.listdir(CURRENT_DIRECTORY)
LOADED = False
usersVideos = []
app = QApplication(sys.argv)
window = None
if 'videos.dictionary' in CURRENT_FILES:
    try:
        usersVideos = loadAll(str(CURRENT_DIRECTORY) + '/videos.dictionary')
        LOADED = True
        window = MainWindow(usersVideos)
    except:
        pass
if not LOADED and 'watch-history.html' in CURRENT_FILES:
    try: 
        window = ProgressWindow(str(CURRENT_DIRECTORY) + '/watch-history.html')
        LOADED = True
    except:
        print('Error loading online, resorting to manual user load...')
if not LOADED:
    window = LoadingWindow()

app.exec()