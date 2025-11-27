# coding:utf-8
from typing import Union

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QPainter, QColor, QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame

from PySide6FluentUI import IconWidget, FluentIcon, isDarkTheme, SingleDirectionScrollArea

from ..utils.url_utils import openUrl
from .sample_card_view import SampleCard


class LinkCard(SampleCard):
    def __init__(self, icon: Union[str, FluentIcon], title: str, content: str, url: Union[str, QUrl], parent: QWidget = None):
        super().__init__(icon, title, content, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.linkIconWidget: IconWidget = IconWidget(FluentIcon.LINK, self)
        self._url: Union[str, QUrl] = url

        self.iconWidget.setFixedSize(52, 52)
        self.titleLabel.setTextColor("black", "white")
        self.contentLabel.setTextColor("gray", "white")
        self.linkIconWidget.setFixedSize(18, 18)

        self.boxLayout.addWidget(self.linkIconWidget, 0, Qt.AlignBottom | Qt.AlignRight)
        self.setFixedSize(200, 234)

    def initLayout(self):
        self.boxLayout: QVBoxLayout = QVBoxLayout(self)
        self.boxLayout.setContentsMargins(26, 26, 16, 16)
        self.boxLayout.addWidget(self.iconWidget, 0, Qt.AlignLeft | Qt.AlignTop)
        self.boxLayout.addWidget(self.titleLabel)
        self.boxLayout.addWidget(self.contentLabel)

    def mouseReleaseEvent(self, event):
        if self._isHover:
            openUrl(self._url)
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if isDarkTheme():
            pc = 255
            c = 39
        else:
            pc = 39
            c = 255
        painter.setPen(QColor(pc, pc, pc, 52 if self._isHover else 26))
        painter.setBrush(QColor(c, c, c, 186 if self._isHover else 211))
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 8, 8)


class LinkCardView(SingleDirectionScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.Orientation.Horizontal)
        self.__initScrollArea()
        self.viewLayout.setAlignment(Qt.AlignLeft)
        self.viewLayout.setSpacing(16)

    def __initScrollArea(self):
        self._widget: QWidget = QWidget()
        self.viewLayout: QHBoxLayout = QHBoxLayout(self._widget)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidget(self._widget)
        self.setWidgetResizable(True)
        self.enableTransparentBackground()

    def addLinkCard(self, icon: Union[str, FluentIcon], title: str, content: str, url: Union[str, QUrl]):
        self.viewLayout.addWidget(LinkCard(icon, title, content, url, self))
