import sys
from PySide6 import QtCore, QtWidgets, QtGui
from pytablericons import TablerIcons, OutlineIcon, FilledIcon
from PIL.ImageQt import ImageQt
from ..utils import commonHelpers as ch
from ..core import ocrService as ocs
import datetime
import os 

def imgToIcon(i, type):
    return QtGui.QPixmap.fromImage(ImageQt(TablerIcons.load(getattr((OutlineIcon if type == 0 else FilledIcon), i.upper()))))

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        fileName = f"/tmp/{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.png"
        extracted_word_boxes = ocs.imgToBoxData(fileName, min_confidence=50) # Adjust confidence as needed
        
        screenLabel = QtWidgets.QLabel(self) 
        screenLabel.setPixmap(QtGui.QPixmap(fileName))
        screenLabel.show()

        try:
            os.remove(fileName)
        except Exception as e:
            print(f"Error removing temporary screenshot file: {e}")

        for item in extracted_word_boxes:   
            textField = QtWidgets.QLineEdit(self)
            # Set the text content
            textField.setText(item["word"].strip()) # Use .strip() to clean up leading spaces from indentation

            textField.setStyleSheet(f"""
                background-color: transparent;
                color: transparent;  
                font-family: Inter;
                font-size: 13px; /* Slightly reduced font size */
                border: 1px solid red;
            """)
            textField.resize(item["width"], item["height"])
            textField.move(item["left"], item["top"])
            textField.show()

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