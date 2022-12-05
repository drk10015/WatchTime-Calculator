import pathlib

from PyQt6 import uic
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from loads.offlineLoader import loadAll
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
            ProgressWindow(self.onlineFileName)

    
    def offlineLoad(self):
        self.onlineFileName = QFileDialog.getOpenFileName(
            self, 'Open file', str(self.CURRENT_PATH), filter= 'dictionary(*.dictionary)')
        if self.onlineFileName[0]:
            self.m = MainWindow(loadAll(self.onlineFileName[0]))
            self.close()
