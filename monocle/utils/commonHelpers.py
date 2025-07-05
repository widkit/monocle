import sys
from PySide6 import QtWidgets # Import QtWidgets to access QApplication

def quitApp():
    app_instance = QtWidgets.QApplication.instance()
    if app_instance:
        sys.exit(app_instance.exec()) # Call exec() on the instance
    else:
        print("Warning: QApplication instance not found. Cannot quit gracefully.")
        sys.exit(1) # Exit with an error code if no app is found

def copySelectedText(imageWidget, notification):
    """Copy selected text to clipboard"""
    if imageWidget:
        selected_text = imageWidget.getSelectedText()
        if selected_text:
            clipboard = QtWidgets.QApplication.clipboard()
            clipboard.setText(selected_text)
            # Show popup notification
            notification.showMessage("✓ Copied to clipboard!")
        else:
            notification.showMessage("⚠ No text selected!")