import sys
from PySide6 import QtWidgets # Import QtWidgets to access QApplication

def quitApp():
    app_instance = QtWidgets.QApplication.instance()
    if app_instance:
        sys.exit(app_instance.exec()) # Call exec() on the instance
    else:
        print("Warning: QApplication instance not found. Cannot quit gracefully.")
        sys.exit(1) # Exit with an error code if no app is found