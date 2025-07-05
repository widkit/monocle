from PySide6 import QtGui
from pytablericons import TablerIcons, OutlineIcon, FilledIcon
from PIL.ImageQt import ImageQt

def imgToIcon(i, type):
    """Convert Tabler icon to QPixmap icon"""
    return QtGui.QPixmap.fromImage(ImageQt(TablerIcons.load(getattr((OutlineIcon if type == 0 else FilledIcon), i.upper())))) 