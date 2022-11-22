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
if 'user.dictionary' in CURRENT_FILES:
    # try:
    user = loadAll(str(CURRENT_DIRECTORY) + '/user.dictionary')
    print(user)
    print('done with load')
    LOADED = True
    window = MainWindow(user)
    # except:
        # pass
if not LOADED and 'watch-history.html' in CURRENT_FILES:
    try: 
        window = ProgressWindow(str(CURRENT_DIRECTORY) + '/watch-history.html')
        LOADED = True
    except:
        print('Error loading online, resorting to manual user load...')
if not LOADED:
    window = LoadingWindow()
window.show()
app.exec()