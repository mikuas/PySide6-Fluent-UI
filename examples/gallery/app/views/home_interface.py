# coding:utf-8
from pathlib import Path
from PySide6.QtCore import Qt
from PySide6FluentUI import VerticalScrollWidget, ImageLabel


class HomeInterface(VerticalScrollWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("HomeInterface")
        self.enableTransparentBackground()
        self.boxLayout.setContentsMargins(0, 0, 0, 0)
        
        # self.image = ImageLabel(str(Path(__file__).resolve().parents[2] / "resources" / "images" / "ATRI.jpg"), self)
        self.image = ImageLabel(":/gallery/images/ATRI.jpg", self)
        self.image.setBorderRadius(8, 8, 8, 8)
        self.image.scaledToHeight(450)
        self.image.scaledToWidth(self.width())
        
        self.addWidget(self.image, 0, Qt.AlignTop)
    
    def resizeEvent(self, e):
        self.image.scaledToHeight(450)
        self.image.scaledToWidth(self.width())