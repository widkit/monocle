from PySide6 import QtCore, QtWidgets, QtGui

class NotificationPopup(QtWidgets.QLabel):
    """Custom popup notification with fade in/out effects and modern styling"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                background-color: #181818;
                color: #fff;
                font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
                font-size: 20px;
                font-weight: 600;
                padding: 18px 48px;
                border-radius: 14px;
                border: 2px solid #fff;
                margin: 0px;
            }
        """)

        # Make it a floating, always-on-top widget
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.Tool |
            QtCore.Qt.WindowStaysOnTopHint
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, False)
        self.setAttribute(QtCore.Qt.WA_ShowWithoutActivating)
        
        # Set up fade effects using QGraphicsOpacityEffect
        self.opacityEffect = QtWidgets.QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacityEffect)
        self.fadeInAnimation = QtCore.QPropertyAnimation(self.opacityEffect, b"opacity")
        self.fadeInAnimation.setDuration(200)
        self.fadeInAnimation.setStartValue(0.0)
        self.fadeInAnimation.setEndValue(1.0)
        self.fadeInAnimation.setEasingCurve(QtCore.QEasingCurve.OutCubic)
        self.fadeOutAnimation = QtCore.QPropertyAnimation(self.opacityEffect, b"opacity")
        self.fadeOutAnimation.setDuration(300)
        self.fadeOutAnimation.setStartValue(1.0)
        self.fadeOutAnimation.setEndValue(0.0)
        self.fadeOutAnimation.setEasingCurve(QtCore.QEasingCurve.InCubic)
        self.fadeOutAnimation.finished.connect(self.hide)
        self.hideTimer = QtCore.QTimer()
        self.hideTimer.setSingleShot(True)
        self.hideTimer.timeout.connect(self.startFadeOut)
        self.hide()
    
    def showMessage(self, message, duration=2000):
        """Show the popup with a message for specified duration"""
        self.setText(message)
        self.adjustSize()
        self.centerInParent()
        self.fadeInAnimation.stop()
        self.fadeOutAnimation.stop()
        self.hideTimer.stop()
        self.opacityEffect.setOpacity(0.0)
        self.show()
        self.raise_()
        self.activateWindow()
        self.fadeInAnimation.start()
        self.hideTimer.start(duration)
    
    def startFadeOut(self):
        self.fadeOutAnimation.start()
    
    def centerInParent(self):
        if self.parent():
            parent_widget = self.parent()
            parent_geometry = parent_widget.geometry()
            parent_global_pos = parent_widget.mapToGlobal(QtCore.QPoint(0, 0))
            popup_size = self.sizeHint()
            x = parent_global_pos.x() + (parent_geometry.width() - popup_size.width()) // 2
            y = parent_global_pos.y() + (parent_geometry.height() - popup_size.height()) // 2
            self.move(x, y) 