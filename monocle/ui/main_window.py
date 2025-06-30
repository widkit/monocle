import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from pytablericons import TablerIcons, OutlineIcon, FilledIcon
from PIL.ImageQt import ImageQt 

def imgToIcon(i):
    return QtGui.QPixmap.fromImage(ImageQt(TablerIcons.load(getattr(OutlineIcon, i.upper()))))

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.copy = QtWidgets.QPushButton("Copy")
        self.search = QtWidgets.QPushButton("Search")
        self.translate = QtWidgets.QPushButton("Translate")
        self.quit = QtWidgets.QPushButton("Quit")

        self.copy.setIcon(imgToIcon("clipboard"))
        self.search.setIcon(imgToIcon("search"))
        self.translate.setIcon(imgToIcon("language"))
        self.quit.setIcon(imgToIcon("x"))

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignBottom)

        self.layout.insertWidget(0, self.copy, 1)
        self.layout.insertWidget(1, self.search, 1)
        self.layout.insertWidget(2, self.translate, 1)
        self.layout.insertWidget(3, self.quit, 1)

    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))

if __name__ == "__main__":
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