from PySide6 import QtCore, QtWidgets

class SelectableOCRBox(QtWidgets.QLineEdit):
    """Custom QLineEdit that can be selected and highlighted"""
    
    def __init__(self, word, parent=None):
        super().__init__(parent)
        self.setText(word.strip())
        self.setReadOnly(True)
        self.isSelected = False
        self.originalWord = word.strip()
        
        self.setStyleSheet("""
            background-color: transparent;
            color: transparent;
            font-family: Inter;
            font-size: 13px;
            padding: 20px;
        """)
        
    def setSelected(self, selected):
        """Set the selection state and update appearance"""
        self.isSelected = selected
        if selected:
            self.setStyleSheet("""
                background-color: rgba(59, 130, 246, 0.8);
                color: transparent;
                font-family: Inter;
                font-size: 13px;
                border: 2px solid rgba(59, 130, 246, 1);
                padding: 20px;
            """)
        else:
            self.setStyleSheet("""
                background-color: transparent;
                color: transparent;
                font-family: Inter;
                font-size: 13px;
                padding: 20px;
            """)
    
    def mousePressEvent(self, event):
        """Handle mouse press to immediately show selection feedback"""
        # Immediately set selected state to show blue highlighting
        self.setSelected(True)
        # Call parent method to handle the actual selection logic
        super().mousePressEvent(event)
