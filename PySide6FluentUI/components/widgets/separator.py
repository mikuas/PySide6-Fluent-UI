# coding:utf-8
from PySide6.QtGui import QPainter, Qt, QColor, QPen
from PySide6.QtWidgets import QWidget

from ...common.config import isDarkTheme


class SeparatorBase(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._color: QColor = None # type: QColor

    def setSeparatorColor(self, color: str | QColor):
        self._color = QColor(color)
        self.update()
        return self


class VerticalSeparator(SeparatorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(3)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        c = 255 if isDarkTheme() else 0
        pen = QPen(self._color or QColor(c, c, c, 32))
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        painter.drawLine(1, 0, 1, self.height())


class HorizontalSeparator(SeparatorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(3)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        c = 255 if isDarkTheme() else 0
        pen = QPen(self._color or QColor(c, c, c, 32))
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        painter.drawLine(0, 1, self.width(), 1)