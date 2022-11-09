import sys
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtCore import QSize, Qt, QAbstractListModel
from PyQt6.QtWidgets import QApplication, QLineEdit, QMainWindow, QPushButton, QLabel, QScrollArea, QWidget, QVBoxLayout, QListWidgetItem

from DetailWindow import DetailWindow
qt_creator_file1 = "mainVideoList.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_creator_file1)
print(Ui_MainWindow)
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, arr) -> None:
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.PERMANENT = []
        # for vid in arr:
        #     vid.thumbnail = 'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBw8QDhUPEBIPDxAQEBAREBAQEBAPDxERFREWFhUVFRgYHSggGBolGxMXIjEjJSkrLi4uFx8zODMsNygtLisBCgoKDg0OGxAQGzUlHyUrKystLS0wKystLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLf/AABEIAOEA4QMBEQACEQEDEQH/xAAbAAEAAgMBAQAAAAAAAAAAAAAABgcBBAUDAv/EAEIQAAIBAgIFBQ0FBwUAAAAAAAABAgMRBAYFEiExQVFxc4GyExQiMzRSU2GRkqHB0TJygrHCBxYjJEKTsxVDYqLh/8QAGgEBAAMBAQEAAAAAAAAAAAAAAAMEBQIBBv/EAC0RAQACAQIEBQQCAgMAAAAAAAABAgMEERIxMlETFCEzcSJBUrFhgQVCI5Gh/9oADAMBAAIRAxEAPwC8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMCN5gzDUw1VQjTU4uCk23JW2tW+BUz6i2O20Qq59RbHbaI3cxZ4nxox6pv6EHn57K8a+ez6/fiXoV/cf0PfPT2e+en8WHnifCjH339B5+exOun8Xw871OFKHvy+h556e37eefn8f2LO9XjSh1SkPPW/H/ANk89b8f228Nnam9lSlOPrjJT+DsSV10feEldbX/AGhItH6So1461KakuKvaS51vRbpkreN4lbpkreN6y3Dt2AAAAAAAAAAAAAAAAAAAAAw2BkD4lTT3pPnVzyY35kxE80MzxoylCMa1OMYOU9SSikk/BbTsuOxmfrMdYiLQztZjrG1oREoqLe0JRjUxVKEknGU0mnua32ZJhiJyREpMMROSIlZM9E4aSs6NFrk1ImvOKnZrzip2RjMWVowg6uHTWqm5U9+xb3H6FLUaSIjiopajSREcVEPKKi2dH42dCoqlN2a4cJLin6jrHeaW3h1jvNLbwtTA4hVaUakd04qS6zbpbirEtuluKIl7NnTp4rG0vPp+/H6nPHXu54q92e+qfnw96I4o7nFHc76p+fD3ojijucUd2O+6d7a8L/fj9RxR3OKO72TOnTIADyqYmEXaUoxfI5JM8m0Q84ohjvun58PeiecVe7zijud9U/Ph70RxR3OKO7DxlJb5wX44jijucVe70p1FJXi01yppo9iXUTu+z0AAAABxM5VJwwFadOUoThBTjKLs01JM5tyV9TMxitMIvl39osXanjUoPd3aC8D8ceHOtnMR0y91TB/kIn0yf9p9hsRCpFThJThJXUotNNepk0NKLRMbwjmfvJodPH/HMp63oj5VNb0R8oGZjMdLLnllHpF+TJcHuwlwe5C0jabT5mroCp9J0e516kFujUmlzKTt8DCyRw3mGFkjhvMNU4lxKzMo37xpX5J+zukrfA2dN7cNnT+3DrVI3VuUmmN42TTG8bIdi8kRUW6VVtpbFNLb1r6FC+hjnWVC+ijnWUQkmnZ7GnZ85Q22UNtubCTexb3uG27zbdNMBkuKcZ1Krck1JxgkldO9rs0MeiiNpmWlj0URtMylyRfXmQMMCP6ZyxDE1HVdScJNJWtGUbIq5tLGS2+6rm00ZJ33QvTOjZYas6UmpbFKMlsvFtr5MzsuKcdtmdlxTjtwtEjRO/oHLTxMO6SnqQu0kleTtv5izg0viRvMreDS+JG8ym+icBHD0lSi3JRu7ytfa7vcaeOkUrww0sWOMdeGG6duwAAAAael8L3bDVaXpKc49bi7P2nlo3hxlrxUmFAuLTs1Zp2ae9Nb0U+T5ufT0dPQOn8Rgp61KV4t+HSl4ufPyP1o6reapcOa+KfpT3T+maWM0fTrUn/vxU4v7UJdzneL9pzq7RbHG3do58tcuGLV7oqZqi6WXPLKPSL8mS4PdhLg92FpXNptPOtUUU5N2STbb3JHkzERvLyZ29VUaRr90r1Ki3TqTkuZydvgYeS3FeZYeS3FeZemitG1MRVVOC2XWvLhGPKz3HjnJbaHWPFOS20LRwlBU6cacdkYRUUvUjbrWKxtDarWKxtD2PXrDAqLGeNn0k+0zCv1T8sK/VPyYPxsOkh2keV6oKdULdRvN1kAAAAQLPy/mYdEu3IzNb1wzNd1wjBTU1jZN8ihzz7TNbS+3DX0vtw7xZWAAAAAederqQcrNqKbaScm7LguLDyZ2jdCq37TMKnaNHESXL4Efg2ReLChP+RxxPKUBzHisPWxEq2HjOEaj1pwmktWfG1nue8hvMTO8M3Nal78VXLOEbo6FqS15Ru9Vx1nHg5Rdk/ZJ+0hz9LqkzydYqJXtg8TKlUjVjbWg7q+7rPa2mtomHtbTW0TDufvnieSj7r+pZ87kWfO5GlpHMGJrx1JySg98YLVT5+Ujyai942lHk1F7xtMtLBSoqd60ZzjyQkovruR04Yn6o9EdJrE/VHonugtKYJxVOhq0n6OS1ZN8/8AU+s08OXFtw19Gphy4tuGvo7yLSyyBhgVJpDx1TpJ9pmFk65+WFk65YwXjqfSQ7SFOqPkp1Qt1G63QAAAAQLP3lMOi/XIy9d1wzNd1wjBTU1kZP8AIaf4+3I2NL7cNfS+3DuFhYAAAABhgV9njJbm5YrCx8N3lVpLZrcXKH/LlXHn3w3x/eGZq9Hv9dFbtW2PY1saexp8hAy+TAG/obxr+4+1Egz9LqnN2ComdPLcU8ZST8/9LJcEb5IhLgjfJCzalGLVnGLXI4po2ZrEtmYiXE0rlehVTcIqlU4SgrRv647rFbJpaW5eivl0tLesekoDjMLOlUlTmrSi7NcOdeoy71ms8Msq1JpPDLxOXKaZP05Kb73qvWdv4cm3dpb4vlNLS55t9FmlpdRNvot/SXl5eYYFS6Q8dU6SfaZhZOuflhZOuWMB46n0tPtoU6o+Ye4+qPmFto3W4yAAAAIFn7ymHRfrkZmu64Zmu64RgpKSycoeQ0/x9uRsaX24bOl9uHbLCcAAAAAAwI9mDKGExnhyTp1fS09kn95bpdZxakW5q2bS48nrPpPdDMV+zXFJ/wAKrRqR4a2tTl1raviRTin7KE/468dM7tWrlPEYJd2rSpNSfc1GEpSd2ta+1Wt4LK2ppNabyjtpb4o4rPEouHUyx5bS+8+yyXT+7CbTe7C0DabIBCM/4ZKdOqt8lKEvXbavzZna2sbxZna2sbxKJFFRbuhqjjiaUlvVWHsbs/gyTDO2SHeGdskbLXNtuMMCpMe71p9JPtMwsnXPywsnXJo/x9PpafbQp1R8w9x9UfMLcRutwAAYuBkCBZ+8ph0X65GXruuGZruuEYKaksnKHkNP8fbkbGl9uGzpfbh2ywnAAGEwMgAAABYCL5+8mh08f8cynrfb/tT1vRHygZmMx0stv+co/f8AkyXB7sJdP7sLSNptAEO/aDUWrShx1py6kkvmUNdPpEKGun0iEMM9nunlvDOpi6aW6MlOXqUdv52XWTaenFkhNp6cWSFomy2WGBUWM8bPpJ9pmFfqn5YV+qfkwXjYdJDtIU6o+XlOqFuo3W8yAAg1fS9WtpGEaNSSpqcYWT8GUU7zbW58fgZts1rZtqz6M22a1s21Z9E4RpNJA8/eUw6JduRma7rhma7rhGCmprHyc/5KHqc1/wB2a2l9uGvpfbh3SysAEWzppZ0oRo05OM5+FJxdnGKfKt13+TKWszTWOGvNS1maaxw15uxl+VR4WnKo3KcoKTb32e1X6rFjDv4cbrGHfw43dElSgAABjWAh+fcbBxhRTTkp68kndpKLSv7xQ1t42isKGtvG0ViUMM9ntnRuJVKvCq9qhOMmlvtxOsduG8WdY7cN4lauGxMKkVODUovc1tRt1tFo3ht1tFo3h9V68YRc5tRildt7Ej2ZiI3l7MxEbyrPMWk++cQ5r7EfBp8PBTe3rMfPl8S+8cvsx8+XxL7xy+zn0aUpyUIJylJ2SSu2QxEzO0IYiZnaFhZX0J3tTcp2dWf2tuyKW6KNbT4PDj15tbT4PDjeebvFlZfNR2TfqPJ5PJ5KhryvOTW5yk/a2YVucsK3OShPVnGXmyi/Y7is7WgrO1oW7Comk07p7nwZuxO8N2J3j0fTZ69RzN2mlRpulB/xaits3wjxb5HyFPVZ+CvDHOVTVZ+CvDHOXGyHg9avKq91OFl96X/iftK+ipvbiV9HTe0ynhqNNX+e5J4teqjBPn15v5oy9bP/ACMvWz/yf0jhUVFh5Jqp4NK+2M5prk23+Zq6SYmjV0k70SC5aWmrpLHwoU3Um7JLYuMnwS9ZxkvFI3lxkyRSN5VtKc8ZilrfaqzSt5sb7l6kjI4py5PlkcU5cnytGlFKKS2JJJcyRsxG0bNqI2jZ9noAADAh2m9FaQq15unN9ybWqu66tlZcOe5QzYc1renL5UM2HPa3pycl5Uxnmw/uRK/lMvZX8pl7Pj918Z6Ne/H6nnlcvY8rl7Ph5Zxvon78PqeeVy9nPlcvZ6YXQ2kabvThVp34xqQXttI6rgz15Rs6rgz15Q2KmgNI1vGNvpKt7dW06nT5783c6fPfm28JkqW+rVSXm002/a/oSU0U/wC0pK6Kf9pSfRmiKGHVqcbN75PwpvnbLmPFXHH0rePFTHH0t9EqV44yc405Sgtaai3FcsrbEeW329HNpmI9EKxdfS9ZOLhOEWrNQjGF0/W3f4mde2pt9mda2pt9nKWXcb6GXtgvmQeXy/j+kMabL+P6Hl7Gegn7YP5nk6bL+P6eTpsv4vSGjNIQ2RhiIrkjJ2+DOvCzx9pe+Fmj7Sy8PpLc44q342Jpn/l7w5/5a3+j4uT20azb3txe1+ts48DJM8nHg5JnknuWdGvD4dRl9uTcp8dr4dS2Gpgx8FNvu1NPj4KbS5mmcbpLu04UKb7mmlCagm34Kvtk7b78CDLfPxbVj0Q5b5+LaseiO19C4+pNznSqSlLa5Nw2/EqWwZrTvMSqWw5rTvMS+Hl3G+gn7YP5jy+X8f088tl/H9Mw0LjobY0qsfuuz+DEYM0coIw5o5Q9O9tJL+nFdTm/mdcOf+XXDn/l4VtHY2f26WInbdrRnK3tOJxZp5xLicWW3OJd/J2g6kKrrVoOGqrQUt92nd25tnWWtJgtWeK0LelwWrPFaExSNBfZAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP/9k='
        for vid in arr:
            self.PERMANENT.append([QListWidgetItem(vid.videoName), vid])
        self.data = self.PERMANENT
        self.searchBar.textEdited.connect(self.search)
        for couple in self.data:
            self.videoView.addItem(couple[0])
        self.videoView.itemDoubleClicked.connect(self.itemDoubleClicked)
        
    def search(self, it):
        for item in self.PERMANENT:
            if not it.lower() in item[0].text().lower():
                item[0].setHidden(True)
            else:
                item[0].setHidden(False)

    def itemDoubleClicked(self, item):
        self.second = DetailWindow(self.getObjectFromItem(item))
        self.second.show()
        # dialog = QtGui.QDialog()
        # dialog.ui = QtGui.Ui_MyDialog()
        # dialog.ui.setupUi(dialog)
        # dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        # dialog.exec_()

    def getObjectFromItem(self, item):
        for couple in self.data:
            if couple[0] == item:
                return couple[1]
    
    



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()