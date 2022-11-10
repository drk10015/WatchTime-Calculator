import pathlib
from PyQt6 import uic
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import QMainWindow, QFileDialog
from loads.offlineLoader import loadAll
from loads.runTimeAPILoader import fetchAPIinfo
from views.ProgressWindow import ProgressWindow


CURRENT_PATH = pathlib.Path(__file__).parent.resolve()
qt_creator_file3 = str(CURRENT_PATH)[:-5] + "/ui/loadingView.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_creator_file3)
Ui_MainWindow3 = Ui_MainWindow
class LoadingWindow(QMainWindow, Ui_MainWindow3):
    def __init__(self) -> None:
        QMainWindow.__init__(self)
        Ui_MainWindow3.__init__(self)
        self.setupUi(self)
        self.onlineLoadButton.clicked.connect(self.onlineLoad)
        self.offlineLoadButton.clicked.connect(self.offlineLoad)
    
    def onlineLoad(self):
        self.onlineFileName = QFileDialog.getOpenFileName(self, 'Open file', str(CURRENT_PATH), filter= 'html(*.html)')
        if self.onlineFileName[0]:
            print(self.onlineFileName[0])
            self.pwindow = ProgressWindow()
            self.pwindow.show()
            fetchAPIinfo(self.onlineFileName[0], self.pwindow)

    def offlineLoad(self):
        self.onlineFileName = QFileDialog.getOpenFileName(
            self, 'Open file', str(CURRENT_PATH), filter= 'dictionary(*.dictionary)')
        if self.onlineFileName[0]:
            print(self.onlineFileName[0])
            loadAll(self.onlineFileName[0])
