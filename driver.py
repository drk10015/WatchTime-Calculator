from runTimeAPILoader import *
from offlineLoader import *
from MainWindowClass import MainWindow
from commandTools import *
from PyQt6.QtWidgets import QApplication
import readline, glob, os, pathlib, sys
from CompletionUtility import Completer
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
    print(usersVideos[300].dateWatched, usersVideos[300].videoName)
    response = input('Save values as Dictionary for quicker loading times? y/n').lower()
    if response == 'y' or response == 'yes':
        saveDictionaryFile(usersVideos)
    # except:
    #     print('Error loading online, resorting to manual user load...')
def commandLine():
    readline.parse_and_bind("tab: complete")
    
    #beginning try to load from default
    if 'videos.dictionary' in CURRENT_FILES:
        try:
            print('Trying to offline load...')
            usersVideos = loadAll('videos.dictionary')
            LOADED = True
            print('Success. Able to load your "videos.dictionary" file.')
        except:
            print('Was unable to find default file, "videos.dictionary" in current directory...\nTrying online load...')
    if not LOADED and 'watch-history.html' in CURRENT_FILES:
        try: 
            print('Trying online load...This may take a few moments...')
            usersVideos = fetchAPIinfo('watch-history.html')
            LOADED = True
            print('Success loading online.')
            response = input('Save values as Dictionary for quicker loading times? y/n').lower()
            if response == 'y' or response == 'yes':
                saveDictionaryFile(usersVideos)
        except:
            print('Error loading online, resorting to manual user load...')
    #manual load if everything fails.
    if not LOADED:
        while True:
            readline.set_completer(loadCompletion)
            choice = (input('please choose a loading method: ')).lower()
            if choice == 'online load':
                readline.set_completer_delims(' \t\n;')
                readline.set_completer(Completer().pathCompleter)
                usersVideos = fetchAPIinfo(input('filename: '))
                response = input('Save values as Dictionary for quicker loading times? y/n').lower()
                if response == 'y' or response == 'yes':
                    saveDictionaryFile(usersVideos)
            elif choice == 'offline pickle':
                readline.set_completer_delims(' \t\n;')
                readline.set_completer(pathCompletion)
                usersVideos = loadAll(input('filename: '))
            elif choice == 'quit' or choice == 'exit' or choice == 'stop' or choice == 'q' or choice == 'e' or choice == 's':
                break

    while True:
        readline.set_completer(driverCompletion)
        choice = input('Please make a selection category: ')
        if choice == 'quit' or choice == 'exit' or choice == 'stop' or choice == 'q' or choice == 'e' or choice == 's':
            break
        elif len(usersVideos) == 0:
            print('You have loaded no videos. Please offline load, online load, or quit the application.')
        elif choice == 'channels':
            readline.set_completer(channelCompletion)
            secondChoice = input('What would you like to do with channels? ')
            line = secondChoice.split(' ')
            choice = line[0]
            if choice == 'search':
                lim = float('inf')
                if '--limit' in line:
                    index = line.index('--limit')
                    lim = int(line[index + 1])
                found = []
                for vid in usersVideos:
                    if (line[1].lower() in vid.channelName.lower()) and not(len(found) >= lim):
                        if not(vid.channelName in found):
                            print(vid.channelName + ' id: ' + vid.channelID)
                            found.append(vid.channelName)
        elif choice == 'videos':
            secondChoice = input('what would you like to do with videos? ')
            if secondChoice[:6] == 'search':
                found = []
                for vid in usersVideos:
                    if secondChoice[7:].lower() in vid.videoName.lower():
                        if not(vid.videoName in found):
                            print(vid.videoName)
                            found.append(vid.videoName)
            elif secondChoice[:17] == 'video watchtime':
                totalTime = 0
                for vid in usersVideos:
                    if secondChoice[18:].lower() == vid.channelName.lower():
                        totalTime += vid.duration
                print(totalTime)
        else:
            print('not a valid command you dumb bitch')


app = QApplication(sys.argv)
window = MainWindow(usersVideos)
window.show()
app.exec()
