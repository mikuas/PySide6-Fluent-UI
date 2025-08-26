# coding:utf-8
from typing import Union
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget, QLayout

from ..layout import VBoxLayout, HBoxLayout
from ..widgets import SingleDirectionScrollArea, SmoothScrollArea, ScrollArea


class SingleScrollWidgetBase(SingleDirectionScrollArea):
    def __init__(self, parent=None, orient: Qt.Orientation = None):
        super().__init__(parent, orient)
        self._widget = QWidget()
        self.boxLayout = None
        self.setWidget(self._widget)
        self.setWidgetResizable(True)

    def addWidget(self, widget: QWidget, stretch=0, alignment=Qt.AlignmentFlag(0)):
        self.boxLayout.addWidget(widget, stretch, alignment)
        return self

    def addLayout(self, layout: QLayout, stretch=0):
        self.boxLayout.addLayout(layout, stretch)

    def addStretch(self, stretch: int):
        self.boxLayout.addStretch(stretch)

    def addSpacing(self, size: int):
        self.boxLayout.addSpacing(size)

    def insertWidget(self, index: int, widget: QWidget, stretch=0, alignment=Qt.AlignmentFlag(0)):
        self.boxLayout.insertWidget(index, widget, stretch, alignment)

    def insertLayout(self, index: int, layout: QLayout, stretch=0):
        self.boxLayout.insertLayout(index, layout, stretch)

    def insertStretch(self, index: int, stretch: int):
        self.boxLayout.insertStretch(index, stretch)

    def insertSpacing(self, index: int, size: int):
        self.boxLayout.insertSpacing(index, size)


class VerticalScrollWidget(SingleScrollWidgetBase):
    """ 平滑垂直滚动小部件 """
    def __init__(self, parent: QWidget = None):
        super().__init__(parent, Qt.Vertical)
        self.boxLayout = VBoxLayout(self._widget)


class HorizontalScrollWidget(SingleScrollWidgetBase):
    """ 平滑水平滚动小部件 """
    def __init__(self, parent: QWidget = None):
        super().__init__(parent, Qt.Horizontal)
        self.boxLayout = HBoxLayout(self._widget)