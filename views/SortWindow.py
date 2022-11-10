import sys, pathlib
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QDialog, QListWidgetItem
import operator


class SortWindow(QDialog):
    def __init__(self, mainWind) -> None:
        QDialog.__init__(self)
        self.CURRENT_PATH = pathlib.Path(__file__).parent.resolve()
        qt_creator_file3 = str(self.CURRENT_PATH)[:-5] + "/ui/sortDialog.ui"
        uic.loadUi(qt_creator_file3, self)
        self.mainWind = mainWind
        self.dateButton.clicked.connect(self.dateClicked)
        self.dateClicked()
        self.sortButton.clicked.connect(self.submitClicked)
        self.videoButton.clicked.connect(self.videoClicked)
        self.channelButton.clicked.connect(self.channelClicked)
        self.durationButton.clicked.connect(self.durationClicked)
        self.show()

    def durationClicked(self):
        self.comboBox.clear()
        self.comboBox.addItems(['least to greatest', 'greatest to least'])

    def channelClicked(self):
        self.comboBox.clear()
        self.comboBox.addItems(['a - z', 'z - a'])

    def videoClicked(self):
        self.comboBox.clear()
        self.comboBox.addItems(['a - z', 'z - a'])

    def dateClicked(self):
        self.comboBox.clear()
        self.comboBox.addItems(['Date Watched (low to high)', 'Date Watched (high to low)'])

    def submitClicked(self):
        if self.durationButton.isChecked():
            newData = sorted(self.mainWind.arr, key=operator.attrgetter('duration'), reverse=self.comboBox.currentIndex())
            self.mainWind.data = newData
            self.mainWind.videoView.clear()
            ret = []
            for vid in newData:
                ret.append([QListWidgetItem(vid.videoName), vid])
            for couple in ret:
                self.mainWind.videoView.addItem(couple[0])
            self.mainWind.data = ret
        elif self.channelButton.isChecked():
            newData = sorted(self.mainWind.arr, key=operator.attrgetter('channelName'), reverse=self.comboBox.currentIndex())
            self.mainWind.data = newData
            self.mainWind.videoView.clear()
            ret = []
            for vid in newData:
                ret.append([QListWidgetItem(vid.channelName + ' - ' + vid.videoName), vid])
            for couple in ret:
                self.mainWind.videoView.addItem(couple[0])
            self.mainWind.data = ret
        elif self.videoButton.isChecked():
            newData = sorted(self.mainWind.arr, key=operator.attrgetter('videoName'), reverse=self.comboBox.currentIndex())
            self.mainWind.data = newData
            self.mainWind.videoView.clear()
            ret = []
            for vid in newData:
                ret.append([QListWidgetItem(vid.videoName), vid])
            for couple in ret:
                self.mainWind.videoView.addItem(couple[0])
            self.mainWind.data = ret
        elif self.dateButton.isChecked():
            if self.comboBox.currentText()[:12] == 'Date Watched':
                newData = sorted(self.mainWind.arr, key=lambda x : x.getDateCode(), reverse=self.comboBox.currentIndex() % 2)
                self.mainWind.data = newData
                self.mainWind.videoView.clear()
                ret = []
                for vid in newData:
                    ret.append([QListWidgetItem(vid.dateWatched + ' - ' + vid.videoName), vid])
                for couple in ret:
                    self.mainWind.videoView.addItem(couple[0])