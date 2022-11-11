import sys, pathlib
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QListWidgetItem
from views.DetailWindow import DetailWindow
from views.SortWindow import SortWindow
import datetime, operator


class MainWindow(QMainWindow):
    def __init__(self, arr) -> None:
        QMainWindow.__init__(self)
        self.CURRENT_PATH = pathlib.Path(__file__).parent.resolve()
        qt_creator_file3 = str(self.CURRENT_PATH)[:-5] + "/ui/mainVideoList.ui"
        uic.loadUi(qt_creator_file3, self)
        self.arr = arr
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

    def itemDoubleClicked(self, item):
        if self.videoButton.isChecked():
            self.second = DetailWindow(self.getObjectFromItem(item))
            self.second.show()

    def getObjectFromItem(self, item):
        for couple in self.data:
            if couple[0] == item:
                return couple[1]
    
    def sortDialog(self):
        self.dialogW = SortWindow(self)
    
    def channelMode(self):
        channels = []
        newData = sorted(self.arr, key=operator.attrgetter('channelName'), reverse=False)
        self.data = []
        for item in newData:
            if not item.channelName in channels:
                self.data.append([QListWidgetItem(item.channelName), item])
                channels.append(item.channelName)
        self.videoView.clear()
        for couple in self.data:
            self.videoView.addItem(couple[0])
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
                ret.append([QListWidgetItem(vid.videoName + ' - ' + vid.channelName), vid])
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
                ret.append([QListWidgetItem(vid.channelName + ' - ' + vid.videoName), vid])
            self.videoView.clear()
            for couple in ret:
                self.videoView.addItem(couple[0])
            self.data = ret
        elif selectedOption == 'Channel':
            channels = []
            newData = sorted(self.arr, key=operator.attrgetter('channelName'), reverse=False)
            self.data = []
            for item in newData:
                if not item.channelName in channels:
                    self.data.append([QListWidgetItem(item.channelName), item])
                    channels.append(item.channelName)
            self.videoView.clear()
            for couple in self.data:
                self.videoView.addItem(couple[0])
        elif selectedOption == 'Duration - Channel':
            channels = []
            newData = sorted(self.arr, key=operator.attrgetter('channelName'), reverse=False)
            self.data = []
            for item in newData:
                if not item.channelName in channels:
                    self.data.append([QListWidgetItem(str(datetime.timedelta(seconds=vid.duration)) + ' - ' + item.channelName), item])
                    channels.append(item.channelName)
            self.videoView.clear()
            for couple in self.data:
                self.videoView.addItem(couple[0])




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()