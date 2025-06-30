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

        self.translate = QtWidgets.QPushButton("Translate")
        self.quit = QtWidgets.QPushButton("Quit")

        self.translate.setIcon(imgToIcon("language"))
        self.quit.setIcon(imgToIcon("x"))

        self.layout = QtWidgets.QHBoxLayout(self)

        self.layout.insertWidget(0, self.translate, 1)
        self.layout.insertWidget(1, self.quit, 1)

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