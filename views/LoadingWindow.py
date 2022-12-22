import pathlib

from PyQt6 import uic
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from loads.offlineLoader import loadAll
from loads.runTimeAPILoader import fetchAPIinfo, saveDictionaryFile
from models.User import User
from views.MainWindowClass import MainWindow
from views.ProgressWindow import ProgressWindow

class LoadingWindow(QMainWindow):
    def __init__(self) -> None:
        QMainWindow.__init__(self)
        self.CURRENT_PATH = pathlib.Path(__file__).parent.resolve()
        qt_creator_file3 = str(self.CURRENT_PATH)[:-5] + "/ui/loadingView.ui"
        uic.loadUi(qt_creator_file3, self)
        self.show()
        self.onlineLoadButton.clicked.connect(self.onlineLoad)
        self.offlineLoadButton.clicked.connect(self.offlineLoad)

    def onlineLoad(self):
        self.onlineFileName = QFileDialog.getOpenFileName(self, 'Open file', str(self.CURRENT_PATH), filter= 'html(*.html)')[0]
        if self.onlineFileName[0]:
            self.close()
            self.pWin = ProgressWindow(beginFunction=self.startLoad, end=self.endLoad)

    def startLoad(self):
        fetchAPIinfo(self.onlineFileName, self.pWin)

    def endLoad(self, result: User):
        saveDictionaryFile('user.dictionary', result)
        self.m = MainWindow(result)
    
    def offlineLoad(self):
        self.onlineFileName = QFileDialog.getOpenFileName(
            self, 'Open file', str(self.CURRENT_PATH), filter= 'dictionary(*.dictionary)')
        if self.onlineFileName[0]:
            self.m = MainWindow(loadAll(self.onlineFileName[0]))
            self.close()
