# coding:utf-8

from PySide6.QtWidgets import QSplitter, QSplitterHandle
from PySide6.QtCore import Qt, QSize, QRectF
from PySide6.QtGui import QPainter, QColor

from ...common.style_sheet import isDarkTheme
from ...common.draw_round_rect import addRoundPath


class SplitterHandle(QSplitterHandle):
    """ SplitterHandle """
    def __init__(self, orientation, parent):
        super().__init__(orientation, parent)
        self.isHover: bool = False

    def enterEvent(self, event):
        self.isHover = True
        self.update()

    def leaveEvent(self, event):
        self.isHover = False
        self.update()

    def sizeHint(self):
        if self.orientation() == Qt.Horizontal:
            return QSize(14, 0)
        else:
            return QSize(0, 14)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = QRectF(self.rect())

        if isDarkTheme():
            pc = 161
            fc = 42
        else:
            pc = 129
            fc = 229

        painter.setBrush(QColor(pc, pc, pc))
        painter.setPen(Qt.NoPen)
        if self.isHover:
            painter.fillPath(addRoundPath(self.rect(), 7, 7, 7, 7), QColor(fc, fc, fc))
        if self.orientation() == Qt.Orientation.Horizontal:
            h = rect.height() // 2 - 16
            painter.drawRoundedRect(rect.adjusted(4.2, h, -4.2, -h), 4, 4)
        else:
            w = rect.width() // 2 - 16
            painter.drawRoundedRect(rect.adjusted(w, 4.4, -w, -4.4), 4, 4)


class Splitter(QSplitter):
    """ Splitter """
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)

    def createHandle(self):
        return SplitterHandle(self.orientation(), self)