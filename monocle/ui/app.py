import sys
from PySide6 import QtWidgets, QtCore
from .mainWindow import mainWindow
from ..utils import imageUtils

def create_and_run_app():
    """Create and run the main application"""
    app = QtWidgets.QApplication(sys.argv)

    primaryScreen = app.primaryScreen()
    screenGeometry = primaryScreen.geometry()
    screenPixelRatio = primaryScreen.devicePixelRatio()

    screenWidth = int(screenGeometry.width() * screenPixelRatio)
    screenHeight = int(screenGeometry.height() * screenPixelRatio)

    # Take screenshot BEFORE showing the main window
    screenshot_filename = imageUtils.grabScreen(screen=primaryScreen)

    widget = mainWindow(screenshot_filename)
    widget.resize(screenWidth, screenHeight)
    widget.show()
    widget.startOCRProcess(screenshot_filename)

    # Start the event loop
    return app.exec()

if __name__ == "__main__":
    create_and_run_app() 