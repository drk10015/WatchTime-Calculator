import sys, pathlib, datetime, time
from PyQt6 import uic, QtGui
from PyQt6.QtCore import *
from PyQt6.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QAbstractItemView, QMenu
from views.DetailWindow import DetailWindow
from views.SortWindow import SortWindow
from views.FilterWindow import FilterWindow
from views.ChannelDetailWindow import ChannelDetailWindow
from models.User import User
from utils.asyncU.Workers import Worker
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
        # self.searchProcess = multiprocessing.Process(target=self.search)
        self.videoMode()
        self.videoView.itemDoubleClicked.connect(self.itemDoubleClicked)
        self.show()
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.search)
        self.searchBar.textChanged.connect(lambda: self.timer.start())
        self.comboBox.currentTextChanged.connect(self.categoryChanged)
        self.channelButton.clicked.connect(self.channelMode)
        self.videoButton.clicked.connect(self.videoMode)
        self.videoView.indexesMoved.connect(self.updateWindow)
        self.videoView.itemSelectionChanged.connect(self.selectionMade)
        # self.clicked.connect(self.updateWindow)
        self.videoView.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.enabledFilters = {'SEARCH': [],
                               'DURATION': [],
                               'YEAR': []}
        self.setWindowTitle('YouTube Calculation Client')
        self._addMenus()
        self.updateWindow()
    
    
    def selectionMade(self):
        if len(self.videoView.selectedItems()) > 0:
            self.itemCountLabel.setText('Selected Item Count: ' + str(len(self.videoView.selectedItems())))
            self.durationLabel.setText('Total Duration of Selected Items: ' + str(datetime.timedelta(seconds= self.getDuration())))
        else:
            self.updateWindow()
    
    def updateWindow(self):
        self.itemCountLabel.setText('Item Count: ' + str(self.getCurrentStats()['count']))
        self.durationLabel.setText('Total Duration of Items: ' + str(datetime.timedelta(seconds= self.getCurrentStats()['duration'])))

    def getCurrentStats(self):
        ret = 0
        dur = 0
        for item in self.data:
            if not item[0].isHidden():
                ret += 1
                if self.videoButton.isChecked():
                    dur += item[1].duration
                else:
                    dur += item[1].getDuration()
        return {'count': ret, 'duration': dur}
    def search(self):
        it = self.searchBar.text()
        if not len(it) == 0:
            for item in self.data:
                if self.videoButton.isChecked():
                    if not (it.lower() in item[0].text().lower()) and not (it.lower() in item[1].dateWatched):
                        self.hiddenStatus('hide', item[0])
                    else:
                        self.hiddenStatus('show', item[0])
                elif self.channelButton.isChecked():
                    if not (it.lower() in item[0].text().lower()):
                        self.hiddenStatus('hide', item[0])
                    else:
                        self.hiddenStatus('show', item[0])
        else:
            for item in self.data:
                self.hiddenStatus('show', item[0])
        self.updateWindow()
        
        
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
        
    def filterDialog(self):
        self.filterD = FilterWindow(self)
    
    def channelMode(self):
        self.data = []
        channels = sorted(self.channels, key=operator.attrgetter('channelTitle'))
        for channel in channels:
            self.data.append([QListWidgetItem(channel.channelTitle), channel])
        self.videoView.clear()
        for couple in self.data:
            self.videoView.addItem(couple[0])
        self.comboBox.clear()
        self.comboBox.addItems(['Channel', 'Duration - Channel', 'Total Videos - Channel'])
    
    def hiddenStatus(self, hide, item):
        obj = ''
        locked = False
        if self.sender() == self.timer:
            obj = 'SEARCH'
        elif self.sender() in self.durationMenuItems:
            obj = 'DURATION'
        else:
            obj = 'YEAR'
        if hide == 'show':
            # if item is in another list, lock it
            for key in self.enabledFilters.keys():
                if key != obj:
                    if (item in self.enabledFilters[key]):
                        locked = True
            # show item if it is not in the previous lists
            if not locked:
                item.setHidden(False)
            # remove item from the senders list
            if item in self.enabledFilters[obj]:
                self.enabledFilters[obj].remove(item)
        else:
            self.enabledFilters[obj].append(item)
            item.setHidden(True)
            
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
                for i in self.data:
                    i[0].setText(i[1].dateWatched[:12] + ' - ' + i[1].videoName)
            elif selectedOption == 'Date - Video (Long)':
                for i in self.data:
                    i[0].setText(i[1].dateWatched + ' - ' + i[1].videoName)
            elif selectedOption == 'Duration - Video':
                for i in self.data:
                    i[0].setText(str(datetime.timedelta(seconds=i[1].duration)) + ' - ' + i[1].videoName)
            elif selectedOption == 'Video - Channel':
                for i in self.data:
                    i[0].setText(i[1].videoName + ' - ' + i[1].getChannelObject(self.user.channels).channelTitle)
            elif selectedOption == 'Channel - Video':
                for i in self.data:
                    i[0].setText(i[1].getChannelObject(self.user.channels).channelTitle + ' - ' + i[1].videoName)
        elif self.channelButton.isChecked():
            if selectedOption == 'Channel':
                for i in self.data:
                    i[0].setText(i[1].channelTitle)
            elif selectedOption == 'Duration - Channel':
                for i in self.data:
                    i[0].setText(str(datetime.timedelta(seconds=i[1].getDuration())) + ' - ' + i[1].channelTitle)
            elif selectedOption == 'Total Videos - Channel':
                for i in self.data:
                    i[0].setText(str(len(i[1].channelVids)) + ' - ' + i[1].channelTitle)

    def _addMenus(self):
        menuBar = self.menuBar()
        # Creating menus using a QMenu object
        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        # Creating menus using a title
        calculationMenu = menuBar.addMenu("&Calculations")
        filterMenu = menuBar.addMenu("&Filter")
        yearMenu = filterMenu.addMenu('&Year')
        for i in range(2005, 2023):
            act = QtGui.QAction(text=str(i), parent=yearMenu, checkable=True)
            act.triggered.connect(self.filterYear)
            self.__setattr__('year' + str(i), act)
            yearMenu.addAction(act)
        durationMenu = filterMenu.addMenu('&Duration')
        greater = durationMenu.addMenu('Greater Than')
        less = durationMenu.addMenu('Less Than')
        self.greater1Mon = QtGui.QAction(text='1 Month', parent=less, checkable=True)
        self.greater1Day = QtGui.QAction(text='1 Day', parent=less, checkable=True)
        self.greater1Hr = QtGui.QAction(text='1 Hour', parent=less, checkable=True)
        self.greater1Min = QtGui.QAction(text='1 Minute', parent=less, checkable=True)
        self.greater1Mon.triggered.connect(lambda : self.filterMinute(1, 2592000))
        self.greater1Day.triggered.connect(lambda : self.filterMinute(1, 86400))
        self.greater1Hr.triggered.connect(lambda : self.filterMinute(1, 3600))
        self.greater1Min.triggered.connect(lambda : self.filterMinute(1, 60))
        greater.addAction(self.greater1Mon)
        greater.addAction(self.greater1Day)
        greater.addAction(self.greater1Hr)
        greater.addAction(self.greater1Min)
        self.less1Mon = QtGui.QAction(text='1 Month', parent=less, checkable=True)
        self.less1Day = QtGui.QAction(text='1 Day', parent=less, checkable=True)
        self.less1Hr = QtGui.QAction(text='1 Hour', parent=less, checkable=True)
        self.less1Min = QtGui.QAction(text='1 Minute', parent=less, checkable=True)
        self.less1Mon.triggered.connect(lambda : self.filterMinute(0, 2592000))
        self.less1Day.triggered.connect(lambda : self.filterMinute(0, 86400))
        self.less1Hr.triggered.connect(lambda : self.filterMinute(0, 3600))
        self.less1Min.triggered.connect(lambda : self.filterMinute(0, 60))
        less.addAction(self.less1Mon)
        less.addAction(self.less1Day)
        less.addAction(self.less1Hr)
        less.addAction(self.less1Min)
        calculationMenu.addAction('Add Durations of Selected').triggered.connect(self.getDuration)
        calculationMenu.addAction('Average Duration of Selected').triggered.connect(self.getAverage)
        self.durationMenuItems = {self.greater1Mon: 2592000,
                                  self.greater1Day: 86400,
                                  self.greater1Hr: 3600,
                                  self.greater1Min: 60,
                                  self.less1Mon: 2592000,
                                  self.less1Day: 86400,
                                  self.less1Hr: 3600,
                                  self.less1Min: 60}
        
    def getDuration(self):
        items = self.videoView.selectedItems()
        ret = 0
        if self.channelButton.isChecked():
            for item in items:
                ret += self.getObjectFromItem(item).getDuration()
        else:
            for item in items:
                ret += self.getObjectFromItem(item).duration
        return ret
    
    def getAverage(self):
        return self.getDuration() / len(self.videoView.selectedItems())

    def getCheckedDurationMenu(self):
        ret = {'less' : None, 'greater' : None}
        for menItem in self.durationMenuItems.keys():
            if menItem.isChecked():
                if menItem == self.greater1Day or menItem == self.greater1Mon or menItem == self.greater1Hr or menItem == self.greater1Min:
                    ret['greater'] = menItem
                else:
                    ret['less'] = menItem
        return ret
    
    def filterMinute(self, sort, timeLength):
        enabled = self.getCheckedDurationMenu()
        for key in self.durationMenuItems.keys():
            if key == enabled['greater']:
                timeLengthMax = self.durationMenuItems[key]
            elif key == enabled['less']:
                timeLengthMin = self.durationMenuItems[key]
        if enabled['greater'] and enabled['less']:
            for item in self.data:
                if (item[1].duration if self.videoButton.isChecked() else item[1].getDuration()) < timeLengthMax or (item[1].duration if self.videoButton.isChecked() else item[1].getDuration()) > timeLengthMin:
                    self.hiddenStatus('hide', item[0])
                else:
                    self.hiddenStatus('show', item[0])
        elif enabled['greater']:
            for item in self.data:
                if (item[1].duration if self.videoButton.isChecked() else item[1].getDuration()) < timeLengthMax:
                    self.hiddenStatus('hide', item[0])
                else:
                    self.hiddenStatus('show', item[0])
        elif enabled['less']:
            for item in self.data:
                if (item[1].duration if self.videoButton.isChecked() else item[1].getDuration()) > timeLengthMin:
                    self.hiddenStatus('hide', item[0])
                else:
                    self.hiddenStatus('show', item[0])
        else:
            for item in self.data:
                self.hiddenStatus('show', item[0])
        self.updateWindow()

    def filterYear(self):
        print(str(len(self.enabledFilters['SEARCH'])))
        sender = self.sender()
        print(self.sender())
        if not sender.isChecked():
            for item in self.data:
                self.hiddenStatus('show', item[0])
        else:
            for i in range(2005, 2023):
                if not self.__getattribute__('year' + str(i)) == sender:
                    self.__getattribute__('year' + str(i)).setChecked(False)
            for i in range(0, len(self.data)):
                if not sender.text() == self.data[i][1].dateWatched.split(',')[1][1:]:
                    self.hiddenStatus('hide', self.data[i][0])
                else:
                    self.hiddenStatus('show', self.data[i][0])
        print(str(len(self.enabledFilters['SEARCH'])))
        self.updateWindow()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()