import sys
from PyQt5 import QtWidgets, uic


class MainWindows(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindows, self).__init__()
        #uic.loadUi(r'./views/mainwindows.ui', self)
        uic.loadUi(r'./views/login.ui', self)


app = QtWidgets.QApplication(sys.argv)
window = MainWindows()

window.show()
app.exec_()