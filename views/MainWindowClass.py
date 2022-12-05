import sys, pathlib
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QListWidgetItem
from views.DetailWindow import DetailWindow
from views.SortWindow import SortWindow
from views.ChannelDetailWindow import ChannelDetailWindow
from models.User import User
import datetime, operator


class MainWindow(QMainWindow):
    def __init__(self, user:User) -> None:
        QMainWindow.__init__(self)
        self.CURRENT_PATH = pathlib.Path(__file__).parent.resolve()
        qt_creator_file3 = str(self.CURRENT_PATH)[:-5] + "/ui/mainVideoList.ui"
        uic.loadUi(qt_creator_file3, self)
        self.user = user
        self.arr = user.videos
        self.channels = user.channels
        self.data = []
        self.comboBox.addItems(['Date - Video (Short)', 'Date - Video (Long)', 'Duration - Video', 'Channel - Video', 'Video - Channel'])
        self.sortButton.clicked.connect(self.sortDialog)
        self.searchBar.textEdited.connect(self.search)
        self.videoMode()
        self.videoView.itemDoubleClicked.connect(self.itemDoubleClicked)
        self.show()
        self.comboBox.currentTextChanged.connect(self.categoryChanged)
        self.channelButton.clicked.connect(self.channelMode)
        self.videoButton.clicked.connect(self.videoMode)
    
    def search(self, it):
        for item in self.data:
            if self.videoButton.isChecked():
                if not (it.lower() in item[0].text().lower()) and not (it.lower() in item[1].dateWatched):
                    item[0].setHidden(True)
                else:
                    item[0].setHidden(False)
            elif self.channelButton.isChecked():
                if not (it.lower() in item[0].text().lower()):
                    item[0].setHidden(True)
                else:
                    item[0].setHidden(False)
    def itemDoubleClicked(self, item):
        if self.videoButton.isChecked():
            self.second = DetailWindow(self, self.getObjectFromItem(item))
            self.second.show()
        if self.channelButton.isChecked():
            self.second = ChannelDetailWindow(self, self.getObjectFromItem(item))
            self.second.show()

    def getObjectFromItem(self, item):
        for couple in self.data:
            if couple[0] == item:
                return couple[1]
    
    def sortDialog(self):
        self.dialogW = SortWindow(self)
    
    def channelMode(self):
        self.data = []
        channels = sorted(self.channels, key=operator.attrgetter('channelTitle'))
        for channel in channels:
            self.data.append([QListWidgetItem(channel.channelTitle), channel])
        self.comboBox.clear()
        self.comboBox.addItems(['Channel', 'Duration - Channel'])

    def videoMode(self):
        self.data = []
        for vid in self.arr:
            self.data.append([QListWidgetItem(vid.dateWatched[:12] + ' - ' + vid.videoName), vid])
        self.videoView.clear()
        for couple in self.data:
            self.videoView.addItem(couple[0])
        self.comboBox.clear()
        self.comboBox.addItems(['Date - Video (Short)', 'Date - Video (Long)', 'Duration - Video', 'Channel - Video', 'Video - Channel'])
    
    def categoryChanged(self):
        selectedOption = self.comboBox.currentText()
        if self.videoButton.isChecked():
            if selectedOption == 'Date - Video (Short)':
                newData = []
                for i in self.data:
                    newData.append(i[1])
                ret = []
                for vid in newData:
                    ret.append([QListWidgetItem(vid.dateWatched[:12] + ' - ' + vid.videoName), vid])
                self.videoView.clear()
                for couple in ret:
                    self.videoView.addItem(couple[0])
                self.data = ret
            elif selectedOption == 'Date - Video (Long)':
                newData = []
                ret = []
                for i in self.data:
                    newData.append(i[1])
                for vid in newData:
                    ret.append([QListWidgetItem(vid.dateWatched + ' - ' + vid.videoName), vid])
                self.videoView.clear()
                for couple in ret:
                    self.videoView.addItem(couple[0])
                self.data = ret
            elif selectedOption == 'Duration - Video':
                newData = []
                ret = []
                for i in self.data:
                    newData.append(i[1])
                for vid in newData:
                    ret.append([QListWidgetItem(str(datetime.timedelta(seconds=vid.duration)) + ' - ' + vid.videoName), vid])
                self.videoView.clear()
                for couple in ret:
                    self.videoView.addItem(couple[0])
                self.data = ret
            elif selectedOption == 'Video - Channel':
                newData = []
                ret = []
                for i in self.data:
                    newData.append(i[1])
                for vid in newData:
                    ret.append([QListWidgetItem(vid.videoName + ' - ' + vid.getChannelObject(self.user.channels).channelTitle), vid])
                self.videoView.clear()
                for couple in ret:
                    self.videoView.addItem(couple[0])
                self.data = ret
            elif selectedOption == 'Channel - Video':
                newData = []
                ret = []
                for i in self.data:
                    newData.append(i[1])
                for vid in newData:
                    ret.append([QListWidgetItem(vid.getChannelObject(self.user.channels).channelTitle + ' - ' + vid.videoName), vid])
                self.videoView.clear()
                for couple in ret:
                    self.videoView.addItem(couple[0])
                self.data = ret
        elif self.channelButton.isChecked():
            if selectedOption == 'Channel':
                newData = []
                ret = []
                for i in self.data:
                    newData.append(i[1])
                for channel in newData:
                    ret.append([QListWidgetItem(channel.channelTitle), channel])
                self.videoView.clear()
                for couple in ret:
                    self.videoView.addItem(couple[0])
                self.data = ret
            elif selectedOption == 'Duration - Channel':
                newData = []
                ret = []
                for i in self.data:
                    newData.append(i[1])
                for channel in newData:
                    ret.append([QListWidgetItem(str(datetime.timedelta(seconds=channel.getDuration())) + ' - ' + channel.channelTitle), channel])
                self.videoView.clear()
                for couple in ret:
                    self.videoView.addItem(couple[0])
                self.data = ret

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()