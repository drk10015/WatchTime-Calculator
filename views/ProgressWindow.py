import pathlib
from PyQt6 import uic
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import QMainWindow


CURRENT_PATH = pathlib.Path(__file__).parent.resolve()
qt_creator_file4 = str(CURRENT_PATH)[:-5] + "/ui/progressWindow.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_creator_file4)
Ui_MainWindow4 = Ui_MainWindow


class ProgressWindow(QMainWindow, Ui_MainWindow4):
    def __init__(self) -> None:
        QMainWindow.__init__(self)
        Ui_MainWindow4.__init__(self)
        self.setupUi(self)

    def setTime(self, remainingTime: float):
        self.etaLabel.setText('Estimated Time Remaining: ' + str(remainingTime) + ' seconds')
    
    def updateProgress(self, percentage):
        self.progressBar.setValue(percentage)