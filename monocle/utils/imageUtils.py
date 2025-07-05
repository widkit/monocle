import tempfile
import os
from PySide6 import QtWidgets

def grabScreen(screen=None):
    app = QtWidgets.QApplication.instance()
    if app is None:
        raise RuntimeError("QApplication must be created before calling grabScreen()")

    # Use provided screen or fall back to primary screen
    if screen is None:
        screen = app.primaryScreen()
    
    screenshot = screen.grabWindow(0)
    
    # Create a temporary file for the screenshot
    temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    temp_filename = temp_file.name
    temp_file.close()
    
    screenshot.save(temp_filename, "png")
    return temp_filename
