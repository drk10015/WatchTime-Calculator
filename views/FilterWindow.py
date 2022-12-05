import pathlib
from PyQt6.QtWidgets import QDialog
from PyQt6 import uic



class FilterWindow(QDialog):
    def __init__(self, mainWind) -> None:
        QDialog.__init__(self)
        self.CURRENT_PATH = pathlib.Path(__file__).parent.resolve()
        qt_creator_file3 = str(self.CURRENT_PATH)[:-5] + "/ui/filterDialog.ui"
        uic.loadUi(qt_creator_file3, self)
        self.mainWind = mainWind
        self.yearLabel.setText(self.comboBox.currentText() + ' Year Recap')
        self.totalVideoLabel = 
        self.show()