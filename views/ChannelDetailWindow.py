import pathlib, urllib
import urllib.request

from PyQt6 import uic, QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from loads.offlineLoader import loadAll
from views.MainWindowClass import MainWindow
from views.ProgressWindow import ProgressWindow
from models.Channel import Channel

class ChannelDetailWindow(QMainWindow):
    def __init__(self, channelObj: Channel) -> None:
        QMainWindow.__init__(self)
        self.CURRENT_PATH = pathlib.Path(__file__).parent.resolve()
        qt_creator_file3 = str(self.CURRENT_PATH)[:-5] + "/ui/channelDetail.ui"
        uic.loadUi(qt_creator_file3, self)
        data = urllib.request.urlopen(channelObj.thumbnail).read()
        img = QtGui.QPixmap()
        img.loadFromData(data)
        self.channelThumbnail.setPixmap(img.scaled(
            341, 201, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.channelTitle.setText(channelObj.channelTitle)
        self.durationLabel.setText(channelObj.timeWatched)
        self.numberVidLabel.setText(len(channelObj.channelVids))