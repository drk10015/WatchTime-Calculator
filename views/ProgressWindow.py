import pathlib
from PyQt6 import uic
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import QDialog
from utils.asyncU.Workers import Worker

class ProgressWindow(QDialog):
    def __init__(self, beginFunction = None, end = None) -> None:
        super(ProgressWindow, self).__init__()
        self.CURRENT_PATH = pathlib.Path(__file__).parent.resolve()
        qt_creator_file3 = str(self.CURRENT_PATH)[:-5] + "/ui/progressWindow.ui"
        uic.loadUi(qt_creator_file3, self)
        self.beginFunc = beginFunction
        self.endFunc = end
        self.threadpool = QThreadPool()
        self.worker = Worker(self.beginFunc)
        self.signals = self.worker.signals
        self.worker.signals.progress.connect(self.updateProgress)
        self.worker.signals.timeRemaining.connect(self.setTime)
        self.worker.signals.result.connect(self.returnedResult)
        self.progressBar.setRange(0,0)
        self.buttonBox.buttons()[0].clicked.connect(self.canceled)
        self.threadpool.start(self.worker)
        self.show()

    def setTime(self, message: str):
        self.etaLabel.setText(message)
    
    def updateProgress(self, percentage, indeterminate = False):
        if indeterminate:
            self.progressBar.setMaximum(0)
        elif self.progressBar.maximum() == 0:
            self.progressBar.setRange(0,100)
        self.progressBar.setValue(percentage)
    
    def returnedResult(self, result: any):
        if self.endFunc: self.endFunc(result)         
        self.close()
    
    def canceled(self):
        self.close()
        exit(1)