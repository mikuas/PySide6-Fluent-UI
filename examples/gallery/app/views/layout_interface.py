# coding:utf-8
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget

from PySide6FluentUI import Splitter, themeColor, drawRoundRect

from ..widgets.basic_interface import Interface

class BackgroundCard(QWidget):
    def __init__(self, radius, parent=None):
        super().__init__(parent)
        self.radius = radius

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(themeColor())
        drawRoundRect(painter, self.rect(), *self.radius)


class LayoutInterface(Interface):
    def __init__(self, parent: QWidget = None):
        super().__init__("布局", "PySide6FluentUI.components.widgets", parent)
        self.setObjectName("LayoutInterface")
        self.vBoxLayout.addWidget(self.scrollArea)

        for o, r in zip([Qt.Orientation.Vertical, Qt.Orientation.Horizontal], [(6, 6, 0, 0), (6, 0, 0, 6)]):
            splitter: Splitter = Splitter(o, self)
            splitter.addWidget(BackgroundCard(r, self))
            splitter.addWidget(QWidget(self))
            splitter.setFixedHeight(224)
            self.addExamplesCard(
                "水平分割器" if o == Qt.Orientation.Vertical else "垂直分割器",
                splitter,
                1
            ).widget.widgetCard.viewLayout.setContentsMargins(0, 0, 0, 0)