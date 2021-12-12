import sys
import utils
from Page import Page
from PyQt5 import QtWidgets as qtw
from PyQt5 import uic
import qdarkstyle


class MainApp(qtw.QApplication):
    """The main application object"""

    def __init__(self, argv):
        super().__init__(argv)

        self.main_window = MainWindow()
        self.main_window.show()
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))


class MainWindow(qtw.QMainWindow):
    """The main application window"""

    def __init__(self):
        super().__init__()
        uic.loadUi("src/ui/main.ui", self)
        self.initBody()


    def initBody(self):
        self.view_page = Page()
        central_layout = self.centralWidget().layout()
        central_layout.addWidget(self.view_page)


if __name__ == '__main__':
    app = MainApp(sys.argv)
    sys.exit(app.exec_())
