import pathlib
from PyQt6 import uic
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import QDialog, QDialogButtonBox
from utils.asyncU.Workers import Worker
from loads.runTimeAPILoader import fetchAPIinfo, saveDictionaryFile
from views.MainWindowClass import MainWindow
from models.User import User

class ProgressWindow(QDialog):
    def __init__(self, loadLink) -> None:
        super(ProgressWindow, self).__init__()
        self.CURRENT_PATH = pathlib.Path(__file__).parent.resolve()
        qt_creator_file3 = str(self.CURRENT_PATH)[:-5] + "/ui/progressWindow.ui"
        uic.loadUi(qt_creator_file3, self)
        self.loadLink = loadLink
        self.threadpool = QThreadPool()
        self.worker = Worker(self.begin)
        self.worker.signals.progress.connect(self.updateProgress)
        self.worker.signals.timeRemaining.connect(self.setTime)
        self.worker.signals.finished.connect(self.end)
        self.worker.signals.result.connect(self.returnedResult)
        self.progressBar.setRange(0,0)
        self.buttonBox.buttons()[0].clicked.connect(self.canceled)
        self.threadpool.start(self.worker)
        self.show()

    def setTime(self, message: str):
        self.etaLabel.setText(message)
    
    def updateProgress(self, percentage):
        if self.progressBar.maximum() == 0:
            self.progressBar.setRange(0,100)
        self.progressBar.setValue(percentage)
    
    def begin(self):
        fetchAPIinfo(self.loadLink, self)
    
    def end(self):
        saveDictionaryFile('user.dictionary', self.user)
        self.m = MainWindow(self.user)
        self.close()
        
    def returnedResult(self, user: User):
        self.user = user
        self.worker.signals.finished.emit()
        
    def canceled(self):
        self.close()
        exit(1)