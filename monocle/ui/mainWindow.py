import sys
from PySide6 import QtCore, QtWidgets, QtGui
from ..utils import commonHelpers as ch
from ..core import ocrService as ocs
from ..utils import imageUtils
from ..utils.iconUtils import imgToIcon
from .imageWidget import ResizableImageWidget
from .notification import NotificationPopup
import os

class mainWindow(QtWidgets.QWidget):
    def __init__(self, screenshot_filename=None):
        super().__init__()

        self.setWindowTitle("Monocle")
        self.setWindowIcon(imgToIcon("screenshot", 0))

        # Initialize layouts
        self.setupLayouts()
        
        # Initialize UI components
        self.setupButtons()
        self.setupNotification()
        
        # Setup the main layout structure
        self.setupMainLayout()

        # Connect signals
        self.quit.clicked.connect(ch.quitApp)
        self.copy.clicked.connect(self.copySelectedText)

        # Store the temporary screenshot filename
        self.screenshot_filename = screenshot_filename

        # Don't start OCR processing immediately - will be called after QApplication is created

    def setupLayouts(self):
        """Initialize all layouts"""
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.imageLayout = QtWidgets.QVBoxLayout()
        self.buttonLayout = QtWidgets.QHBoxLayout()
        
        # Set layout properties
        self.buttonLayout.setAlignment(QtCore.Qt.AlignBottom)

    def setupButtons(self):
        """Create and configure buttons"""
        self.copy = QtWidgets.QPushButton("Copy")
        self.search = QtWidgets.QPushButton("Search")
        self.translate = QtWidgets.QPushButton("Translate")
        self.quit = QtWidgets.QPushButton("Quit")

        # Set button icons
        self.copy.setIcon(imgToIcon("clipboard", 0))
        self.search.setIcon(imgToIcon("search", 0))
        self.translate.setIcon(imgToIcon("language", 0))
        self.quit.setIcon(imgToIcon("x", 0))

        # Add buttons to layout
        self.buttonLayout.addWidget(self.copy)
        self.buttonLayout.addWidget(self.search)
        self.buttonLayout.addWidget(self.translate)
        self.buttonLayout.addWidget(self.quit)

    def setupMainLayout(self):
        """Setup the main layout hierarchy"""
        # Add image layout (will be populated after OCR)
        self.mainLayout.addLayout(self.imageLayout, 1)
        
        # Add button layout at bottom
        self.mainLayout.addLayout(self.buttonLayout)

    def setupNotification(self):
        """Setup the notification popup"""
        self.notification = NotificationPopup(self)

    def copySelectedText(self):
        """Copy selected text to clipboard using commonHelpers"""
        ch.copySelectedText(getattr(self, 'imageWidget', None), self.notification)

    def resizeEvent(self, event):
        """Handle main window resize to reposition notification"""
        super().resizeEvent(event)
        if hasattr(self, 'notification') and self.notification.isVisible():
            self.notification.centerInParent()

    def startOCRProcess(self, screenshot_filename):
        """Start the OCR processing workflow"""
        try:
            # Store the screenshot filename
            self.screenshot_filename = screenshot_filename
            
            # Show processing notification
            QtCore.QTimer.singleShot(0, lambda: self.notification.showMessage("Processing OCR...", 2000))
            
            # Screenshot already taken in app.py, just load and process
            self.loadScreenshot()
            QtCore.QTimer.singleShot(200, self.processOCR)
        except Exception as e:
            print(f"Error in OCR process: {e}")
            self.notification.showMessage("OCR Process Error!", 3000)

    def loadScreenshot(self):
        """Load and display the screenshot"""
        try:
            # Create the resizable image widget
            self.imageWidget = ResizableImageWidget(self)
            self.imageWidget.setPixmap(QtGui.QPixmap(self.screenshot_filename))
            self.imageWidget.setFocusPolicy(QtCore.Qt.StrongFocus)  # Enable keyboard focus
            
            # Add to layout
            self.imageLayout.addWidget(self.imageWidget)
            
        except Exception as e:
            print(f"Error loading screenshot: {e}")
            self.notification.showMessage("Image Load Error!", 3000)

    def processOCR(self):
        """Process OCR and create text boxes"""
        extracted_word_boxes = []
        try:
            extracted_word_boxes = ocs.imgToBoxData(self.screenshot_filename, min_confidence=30)
        except Exception as e:
            print(f"Error running Pytesseract: {e}")
            self.notification.showMessage("OCR Error!", 3000)
            return

        # Clean up temporary file
        try:
            os.remove(self.screenshot_filename)
        except Exception as e:
            print(f"Error removing temporary screenshot file: {e}")

        # Create text boxes for OCR results
        self.createOCRBoxes(extracted_word_boxes)
        
        # Show completion notification
        self.notification.showMessage("✓ OCR Complete!", 2000)

    def createOCRBoxes(self, extracted_word_boxes):
        """Create text boxes for OCR results"""
        for item in extracted_word_boxes:
            self.imageWidget.addOCRBox(
                item["word"],
                int(item["left"]),
                int(item["top"]),
                item["width"],
                item["height"]
            )