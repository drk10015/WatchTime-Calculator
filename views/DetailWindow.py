from PyQt6 import QtGui, uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow
import datetime, sys, os, pathlib
import urllib.request

# from ui_detailwindow import Ui_MainWindow
CURRENT_PATH = pathlib.Path(__file__).parent.resolve()
qt_creator_file2 = str(CURRENT_PATH)[:-5] + "/ui/detailView.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_creator_file2)
Ui_MainWindow2 = Ui_MainWindow

class DetailWindow(QMainWindow, Ui_MainWindow2):
    def __init__(self, mainWindow, vid) -> None:
        QMainWindow.__init__(self)
        Ui_MainWindow2.__init__(self)
        self.setupUi(self)
        data = urllib.request.urlopen(vid.thumbnail).read()
        img = QtGui.QPixmap()
        img.loadFromData(data)
        self.thumbnail.setPixmap(img.scaled(
            341, 201, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.label.setText(vid.videoName)
        self.label_2.setText(vid.getChannelObject(mainWindow.user.channels).channelTitle)
        self.label_3.setText(str(datetime.timedelta(seconds=vid.duration)))
        self.descriptionLabel.setText(vid.description)
        self.dateWatchedLabel.setText(vid.dateWatched)
        # self.show()
        # print(self)
        

    def search(self, it):
        for item in self.PERMANENT:
            if not it.lower() in item[0].text().lower():
                item[0].setHidden(True)
            else:
                item[0].setHidden(False)

    def clicked(self, qmodelindex):
        item = self.videoView.currentItem()
        print(item.text())

    def itemClicked(self, item):
        print(self.getObjectFromItem(item).channelName)

    def getObjectFromItem(self, item):
        for couple in self.data:
            if couple[0] == item:
                return couple[1]

    def resetLabels(self):
        for couple in self.data:
            self.videoView.addItem(couple[0])
