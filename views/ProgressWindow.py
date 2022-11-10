import pathlib
from PyQt6 import uic
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import QDialog
from utils.asyncU.Workers import Worker
from loads.runTimeAPILoader import fetchAPIinfo, saveDictionaryFile
from views.MainWindowClass import MainWindow

class ProgressWindow(QDialog):
    def __init__(self, loadLink) -> None:
        super(ProgressWindow, self).__init__()
        self.CURRENT_PATH = pathlib.Path(__file__).parent.resolve()
        qt_creator_file3 = str(self.CURRENT_PATH)[:-5] + "/ui/progressWindow.ui"
        uic.loadUi(qt_creator_file3, self)
        self.loadLink = loadLink
        self.buttonBox.clicked.connect(self.begin)
        self.threadpool = QThreadPool()
        self.worker = Worker(self.begin)
        self.worker.signals.progress.connect(self.updateProgress)
        self.worker.signals.timeRemaining.connect(self.setTime)
        self.worker.signals.finished.connect(self.end)
        self.worker.signals.result.connect(self.returnedResult)
        self.threadpool.start(self.worker)
        self.show()

    def setTime(self, remainingTime: float):
        self.etaLabel.setText('Estimated Time Remaining: ' + str(remainingTime) + ' seconds')
    
    def updateProgress(self, percentage):
        print('My percentage = ', str(percentage))
        self.progressBar.setValue(percentage)
    
    def begin(self):
        self.usersVideos = fetchAPIinfo(self.loadLink, self)
        print(self.usersVideos)
    
    def end(self):
        saveDictionaryFile(self.usersVideos)
        self.m = MainWindow(self.usersVideos)
        self.close()
        
    def returnedResult(self, vids):
        self.usersVideos = vids
        print(self.usersVideos)
        self.worker.signals.finished.emit()
        