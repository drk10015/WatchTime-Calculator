import datetime
import operator
import pathlib
import sys, time

from views.ProgressWindow import ProgressWindow
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QListWidgetItem


class SortWindow(QDialog):
    def __init__(self, mainWind) -> None:
        QDialog.__init__(self, None, )
        self.CURRENT_PATH = pathlib.Path(__file__).parent.resolve()
        qt_creator_file3 = str(self.CURRENT_PATH)[:-5] + "/ui/sortDialog.ui"
        uic.loadUi(qt_creator_file3, self)
        self.mainWind = mainWind
        self.dateButton.clicked.connect(self.dateClicked)
        self.dateClicked()
        self.progressBar.setHidden(True)
        self.sortButton.clicked.connect(self.submitClicked)
        self.videoButton.clicked.connect(self.videoClicked)
        self.channelButton.clicked.connect(self.channelClicked)
        self.durationButton.clicked.connect(self.durationClicked)
        self.totalVideoButton.clicked.connect(self.numberClicked)
        self.mainWind.channelButton.clicked.connect(self.updateWindow)
        self.mainWind.videoButton.clicked.connect(self.updateWindow)

        self.setWindowTitle('Sort')
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.updateWindow()
        self.show()
    def updateWindow(self):
        self.videoButton.setHidden(False) if self.mainWind.videoButton.isChecked() else self.videoButton.setHidden(True)
        self.totalVideoButton.setHidden(False) if self.mainWind.channelButton.isChecked() else self.totalVideoButton.setHidden(True)
    
    def durationClicked(self):
        self.comboBox.clear()
        self.comboBox.addItems(['least to greatest', 'greatest to least'])

    def channelClicked(self):
        self.comboBox.clear()
        self.comboBox.addItems(['a - z', 'z - a'])

    def videoClicked(self):
        self.comboBox.clear()
        self.comboBox.addItems(['a - z', 'z - a'])

    def numberClicked(self):
        self.comboBox.clear()
        self.comboBox.addItems(['least to greatest', 'greatest to least'])

    def dateClicked(self):
        self.comboBox.clear()
        self.comboBox.addItems(['Date Watched (recent to furthest)','Date Watched (furthest to recent)'])

    def getIndex(self, obj):
        for i in range(0, len(self.mainWind.data)):
            if self.mainWind.data[i][0] == obj:
                return i
    
    def submitClicked(self):
        # self.mainWind.pWin = ProgressWindow(self.sort)
        self.sort()
    
    def sort(self):
        self.mainWind.toggleLoading()
        self.progressBar.setHidden(False)
        length = self.mainWind.videoView.count()
        if self.mainWind.videoButton.isChecked():
            ret = []
            if self.durationButton.isChecked():
                begin = time.perf_counter()
                # self.mainWind.pWin.signals.timeRemaining.emit('We are working on this...')
                # self.mainWind.pWin.signals.progress.emit(0, True)
                for i in range(0, length):
                    self.mainWind.videoView.takeItem(0)
                    # self.mainWind.pWin.signals.progress.emit(int((i / length) * 100), False)
                    # self.mainWind.pWin.signals.timeRemaining.emit('Current time: ' + str(time.perf_counter() - begin))
                print('deletion time: ', str(time.perf_counter() - begin))
                begin = time.perf_counter()
                newData = sorted(self.mainWind.data, key=(lambda couple : couple[1].duration), reverse=(not self.comboBox.currentIndex()))
                print('sort time: ', str(time.perf_counter() - begin))
                begin = time.perf_counter()
                self.mainWind.data = newData 
                for i in range(0,len(newData)):
                    self.mainWind.videoView.insertItem(0, newData[i][0])
                print('insertion time: ', str(time.perf_counter() - begin))
                begin = time.perf_counter()
                for i in range(0,len(newData)): 
                    self.mainWind.fixHidden(newData[i][0])
                print('fixed hidden time: ', str(time.perf_counter() - begin))

            elif self.channelButton.isChecked():
                newData = sorted(self.mainWind.arr, key=lambda video: video.getChannelObject(self.mainWind.user.channels).channelTitle, reverse=self.comboBox.currentIndex())
                self.mainWind.videoView.clear()
                for vid in newData:
                    ret.append([QListWidgetItem(vid.getChannelObject(self.mainWind.user.channels).channelTitle + ' - ' + vid.videoName), vid])
                for couple in ret:
                    self.mainWind.videoView.addItem(couple[0])
            elif self.videoButton.isChecked():
                newData = sorted(self.mainWind.arr, key=operator.attrgetter('videoName'), reverse=self.comboBox.currentIndex())
                self.mainWind.videoView.clear()
                for vid in newData:
                    ret.append([QListWidgetItem(vid.videoName), vid])
                for couple in ret:
                    self.mainWind.videoView.addItem(couple[0])
            elif self.dateButton.isChecked():
                if self.comboBox.currentText()[:12] == 'Date Watched':
                    newData = sorted(self.mainWind.arr, key=lambda x:x.getDateCode(), reverse=not(self.comboBox.currentIndex() % 2))
                    self.mainWind.videoView.clear()
                    for vid in newData:
                        ret.append([QListWidgetItem(vid.dateWatched + ' - ' + vid.videoName), vid])
                    for couple in ret:
                        self.mainWind.videoView.addItem(couple[0])

        elif self.mainWind.channelButton.isChecked():
            ret = []
            if self.durationButton.isChecked():
                newData = sorted(self.mainWind.channels, key=lambda channel: channel.getDuration(), reverse=self.comboBox.currentIndex())
                self.mainWind.videoView.clear()
                for channel in newData:
                    ret.append([QListWidgetItem(str(datetime.timedelta(
                        seconds=channel.getDuration())) + ' - ' + channel.channelTitle), channel])
                for couple in ret:
                    self.mainWind.videoView.addItem(couple[0])
            elif self.channelButton.isChecked():
                newData = sorted(self.mainWind.channels, key=lambda channel: channel.channelTitle, reverse=self.comboBox.currentIndex())
                self.mainWind.videoView.clear()
                for channel in newData:
                    ret.append([QListWidgetItem(channel.channelTitle), channel])
                for couple in ret:
                    self.mainWind.videoView.addItem(couple[0])
            elif self.dateButton.isChecked():
                if self.comboBox.currentText()[:12] == 'Date Watched':
                    newData = sorted(self.mainWind.channels, key=lambda channel: channel.getRecentVideos()[0].getDateCode(), reverse=self.comboBox.currentIndex())
                    self.mainWind.videoView.clear()
                    for channel in newData:
                        ret.append(
                            [QListWidgetItem(channel.getRecentVideos()[0].dateWatched + ' - ' + channel.channelTitle), channel])
                    for couple in ret:
                        self.mainWind.videoView.addItem(couple[0])
            elif self.totalVideoButton.isChecked():
                newData = sorted(self.mainWind.channels, key=lambda channel: len(channel.channelVids), reverse=self.comboBox.currentIndex())
                self.mainWind.videoView.clear()
                for channel in newData:
                    ret.append(
                        [QListWidgetItem(str(len(channel.channelVids)) + ' - ' + channel.channelTitle), channel])
                for couple in ret:
                    self.mainWind.videoView.addItem(couple[0])
            self.mainWind.data = ret
            self.mainWind.categoryChanged()
        self.mainWind.toggleLoading()
        self.progressBar.setHidden(True)
        # self.mainWind.pWin.signals.result.emit(True)

