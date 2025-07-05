from PySide6 import QtCore, QtWidgets, QtGui
from .customWidgets import SelectableOCRBox

class ResizableImageWidget(QtWidgets.QWidget):
    """Custom widget that displays an image with resizable OCR text boxes"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.originalPixmap = None
        self.scaledPixmap = None
        self.ocrBoxes = []
        self.selectedBoxes = []
        self.originalImageSize = QtCore.QSize()
        self.scaleFactor = 1.0
        
        # Selection variables
        self.isSelecting = False
        self.selectionStart = QtCore.QPoint()
        self.selectionEnd = QtCore.QPoint()
        self.selectionRect = QtCore.QRect()
        
        # Enable mouse tracking for selection
        self.setMouseTracking(True)
        
    def setPixmap(self, pixmap):
        """Set the image pixmap and store original size"""
        self.originalPixmap = pixmap
        self.originalImageSize = pixmap.size()
        self.updateScaledPixmap()
        
    def updateScaledPixmap(self):
        """Update the scaled pixmap based on current widget size"""
        if self.originalPixmap is None:
            return
            
        # Calculate scale factor to fit image in widget while maintaining aspect ratio
        widget_size = self.size()
        if widget_size.width() == 0 or widget_size.height() == 0:
            return
            
        scale_x = widget_size.width() / self.originalImageSize.width()
        scale_y = widget_size.height() / self.originalImageSize.height()
        self.scaleFactor = min(scale_x, scale_y)
        
        # Scale the pixmap
        scaled_size = self.originalImageSize * self.scaleFactor
        self.scaledPixmap = self.originalPixmap.scaled(
            scaled_size, 
            QtCore.Qt.KeepAspectRatio, 
            QtCore.Qt.SmoothTransformation
        )
        
        # Update OCR box positions
        self.updateOCRBoxPositions()
        self.update()
        
    def addOCRBox(self, word, left, top, width, height):
        """Add an OCR text box with original coordinates"""
        textField = SelectableOCRBox(word, self)
        
        # Store original coordinates
        box_data = {
            'widget': textField,
            'original_left': left,
            'original_top': top,
            'original_width': width,
            'original_height': height
        }
        
        self.ocrBoxes.append(box_data)
        self.updateOCRBoxPositions()
        textField.show()
        
    def updateOCRBoxPositions(self):
        """Update OCR box positions based on current scale factor"""
        if not self.scaledPixmap:
            return
            
        # Calculate image position (centered in widget)
        widget_size = self.size()
        image_size = self.scaledPixmap.size()
        
        image_x = (widget_size.width() - image_size.width()) // 2
        image_y = (widget_size.height() - image_size.height()) // 2
        
        # Update each OCR box
        for box_data in self.ocrBoxes:
            widget = box_data['widget']
            
            # Scale and position the box
            scaled_left = int(box_data['original_left'] * self.scaleFactor) + image_x
            scaled_top = int(box_data['original_top'] * self.scaleFactor) + image_y
            scaled_width = int(box_data['original_width'] * self.scaleFactor)
            scaled_height = int(box_data['original_height'] * self.scaleFactor)
            
            widget.setGeometry(scaled_left, scaled_top, scaled_width, scaled_height)
            
    def handleBoxSelection(self, box, event):
        """Handle individual box selection"""
        modifiers = event.modifiers()
        
        if modifiers & QtCore.Qt.ControlModifier:
            # Ctrl+Click: Toggle selection
            if box.isSelected:
                self.deselectBox(box)
            else:
                self.selectBox(box)
        else:
            # Regular click: Select only this box
            self.clearSelection()
            self.selectBox(box)
            
    def selectBox(self, box):
        """Select a specific box"""
        if box not in self.selectedBoxes:
            self.selectedBoxes.append(box)
            box.setSelected(True)
            
    def deselectBox(self, box):
        """Deselect a specific box"""
        if box in self.selectedBoxes:
            self.selectedBoxes.remove(box)
            box.setSelected(False)
            
    def clearSelection(self):
        """Clear all selected boxes"""
        for box in self.selectedBoxes:
            box.setSelected(False)
        self.selectedBoxes.clear()
        
    def selectBoxesInRect(self, rect):
        """Select all boxes that intersect with the given rectangle"""
        for box_data in self.ocrBoxes:
            widget = box_data['widget']
            box_rect = widget.geometry()
            
            if rect.intersects(box_rect):
                self.selectBox(widget)
                
    def getSelectedText(self):
        """Get the text from all selected boxes"""
        return ' '.join([box.originalWord for box in self.selectedBoxes])
        
    def mousePressEvent(self, event):
        """Handle mouse press for area selection"""
        if event.button() == QtCore.Qt.LeftButton:
            # Check if we clicked on empty space (not on a box)
            child = self.childAt(event.pos())
            if child is None or not isinstance(child, SelectableOCRBox):
                # Start area selection
                self.isSelecting = True
                self.selectionStart = event.pos()
                self.selectionEnd = event.pos()
                
                # Clear selection if not holding Ctrl
                if not (event.modifiers() & QtCore.Qt.ControlModifier):
                    self.clearSelection()
                    
        super().mousePressEvent(event)
        
    def mouseMoveEvent(self, event):
        """Handle mouse move for area selection"""
        if self.isSelecting:
            self.selectionEnd = event.pos()
            self.selectionRect = QtCore.QRect(self.selectionStart, self.selectionEnd).normalized()
            self.update()  # Repaint to show selection rectangle
            
        super().mouseMoveEvent(event)
        
    def mouseReleaseEvent(self, event):
        """Handle mouse release to complete selection"""
        if self.isSelecting and event.button() == QtCore.Qt.LeftButton:
            self.isSelecting = False
            
            # Select boxes in the selection rectangle
            if self.selectionRect.width() > 5 and self.selectionRect.height() > 5:
                self.selectBoxesInRect(self.selectionRect)
                
            self.selectionRect = QtCore.QRect()
            self.update()  # Repaint to remove selection rectangle
            
        super().mouseReleaseEvent(event)
        
    def keyPressEvent(self, event):
        """Handle keyboard shortcuts"""
        if event.key() == QtCore.Qt.Key_A and event.modifiers() & QtCore.Qt.ControlModifier:
            # Ctrl+A: Select all boxes
            self.clearSelection()
            for box_data in self.ocrBoxes:
                self.selectBox(box_data['widget'])
        elif event.key() == QtCore.Qt.Key_C and event.modifiers() & QtCore.Qt.ControlModifier:
            # Ctrl+C: Copy selected text
            selected_text = self.getSelectedText()
            if selected_text:
                clipboard = QtWidgets.QApplication.clipboard()
                clipboard.setText(selected_text)
                # Show popup notification via parent
                if hasattr(self.parent(), 'notification'):
                    self.parent().notification.showMessage("✓ Copied to clipboard!")
            else:
                if hasattr(self.parent(), 'notification'):
                    self.parent().notification.showMessage("⚠ No text selected!")
        elif event.key() == QtCore.Qt.Key_Escape:
            # Escape: Clear selection
            self.clearSelection()
            
        super().keyPressEvent(event)
            
    def paintEvent(self, event):
        """Paint the scaled image centered in the widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
        
        # Draw the scaled image
        if self.scaledPixmap is not None:
            # Calculate position to center the image
            widget_size = self.size()
            image_size = self.scaledPixmap.size()
            
            x = (widget_size.width() - image_size.width()) // 2
            y = (widget_size.height() - image_size.height()) // 2
            
            painter.drawPixmap(x, y, self.scaledPixmap)
        
        # Draw selection rectangle
        if self.isSelecting and not self.selectionRect.isEmpty():
            painter.setPen(QtGui.QPen(QtCore.Qt.blue, 1, QtCore.Qt.DashLine))
            painter.setBrush(QtGui.QBrush(QtCore.Qt.blue, QtCore.Qt.NoBrush))
            painter.drawRect(self.selectionRect)
        
    def resizeEvent(self, event):
        """Handle widget resize events"""
        super().resizeEvent(event)
        self.updateScaledPixmap() 