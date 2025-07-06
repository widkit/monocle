import sys
from PySide6 import QtWidgets, QtCore
from .mainWindow import mainWindow
from ..utils import imageUtils

def runApp():
    """Create and run the main application"""
    app = QtWidgets.QApplication(sys.argv)

    primaryScreen = app.primaryScreen()
    screenGeometry = primaryScreen.geometry()
    screenPixelRatio = primaryScreen.devicePixelRatio()

    screenWidth = int(screenGeometry.width() * screenPixelRatio)
    screenHeight = int(screenGeometry.height() * screenPixelRatio)

    # Take screenshot BEFORE showing the main window
    screenshotFilename = imageUtils.grabScreen(screen=primaryScreen)

    widget = mainWindow(screenshotFilename)
    widget.resize(screenWidth, screenHeight)
    widget.show()
    widget.startOCRProcess(screenshotFilename)

    # Start the event loop
    return app.exec()

if __name__ == "__main__":
    runApp() 