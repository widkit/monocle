import sys
from PySide6 import QtCore, QtWidgets, QtGui
from pytablericons import TablerIcons, OutlineIcon, FilledIcon
from PIL.ImageQt import ImageQt
from ..utils import common_helpers as ch

def imgToIcon(i, type):
    return QtGui.QPixmap.fromImage(ImageQt(TablerIcons.load(getattr((OutlineIcon if type == 0 else FilledIcon), i.upper()))))

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Monocle")
        self.setWindowIcon(imgToIcon("screenshot", 0))

        self.copy = QtWidgets.QPushButton("Copy")
        self.search = QtWidgets.QPushButton("Search")
        self.translate = QtWidgets.QPushButton("Translate")
        self.quit = QtWidgets.QPushButton("Quit")

        self.copy.setIcon(imgToIcon("clipboard", 0))
        self.search.setIcon(imgToIcon("search", 0))
        self.translate.setIcon(imgToIcon("language", 0))
        self.quit.setIcon(imgToIcon("x", 0))

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignBottom)

        self.layout.insertWidget(0, self.copy, 1)
        self.layout.insertWidget(1, self.search, 1)
        self.layout.insertWidget(2, self.translate, 1)
        self.layout.insertWidget(3, self.quit, 1)

        # self.copy.clicked.connect()
        # self.search.clicked.connect()
        # self.translate.clicked.connect()
        self.quit.clicked.connect(ch.quitApp)

app = QtWidgets.QApplication([])

primaryScreen = app.primaryScreen()
screenGeometry = primaryScreen.geometry()
screenPixelRatio = primaryScreen.devicePixelRatio()

screenWidth = int(screenGeometry.width() * screenPixelRatio)
screenHeight = int(screenGeometry.height() * screenPixelRatio)

widget = MyWidget()
widget.resize(screenWidth, screenHeight)
widget.show()

sys.exit(app.exec())