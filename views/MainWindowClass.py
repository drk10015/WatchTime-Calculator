import sys, pathlib
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QListWidgetItem
from views.DetailWindow import DetailWindow


class MainWindow(QMainWindow):
    def __init__(self, arr) -> None:
        QMainWindow.__init__(self)
        self.CURRENT_PATH = pathlib.Path(__file__).parent.resolve()
        qt_creator_file3 = str(self.CURRENT_PATH)[:-5] + "/ui/mainVideoList.ui"
        uic.loadUi(qt_creator_file3, self)
        self.PERMANENT = []
        for vid in arr:
            self.PERMANENT.append([QListWidgetItem(vid.videoName), vid])
        self.data = self.PERMANENT
        self.searchBar.textEdited.connect(self.search)
        for couple in self.data:
            self.videoView.addItem(couple[0])
        self.videoView.itemDoubleClicked.connect(self.itemDoubleClicked)
        self.show()
        
    def search(self, it):
        for item in self.PERMANENT:
            if not it.lower() in item[0].text().lower():
                item[0].setHidden(True)
            else:
                item[0].setHidden(False)

    def itemDoubleClicked(self, item):
        self.second = DetailWindow(self.getObjectFromItem(item))
        self.second.show()

    def getObjectFromItem(self, item):
        for couple in self.data:
            if couple[0] == item:
                return couple[1]
    
    



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()