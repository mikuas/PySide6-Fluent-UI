# coding:utf-8
from typing import Union

from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor, QIcon, QFont
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame

from PySide6FluentUI import IconWidget, FluentIcon, isDarkTheme, CaptionLabel, FlowLayout, SubtitleLabel


class SampleCard(QFrame):
    def __init__(self, icon: Union[str, FluentIcon, QIcon], title: str, content: str, parent=None):
        super().__init__(parent)
        self._isHover: bool = False
        self.iconWidget: IconWidget = IconWidget(icon, self)
        self.titleLabel: SubtitleLabel = SubtitleLabel(title, self)
        self.contentLabel: CaptionLabel = CaptionLabel(content, self)

        self.contentLabel.setWordWrap(True)
        self.titleLabel.setFontSize(15, QFont.Weight.Bold)
        self.contentLabel.setTextColor("gray", "white")
        self.iconWidget.setFixedSize(42, 42)
        self.setFixedSize(300, 80)
        self.initLayout()

    def initLayout(self):
        self.boxLayout: QHBoxLayout = QHBoxLayout(self)
        self.textLayout: QVBoxLayout = QVBoxLayout()
        self.boxLayout.setContentsMargins(16, 12, 12, 16)
        self.textLayout.setContentsMargins(16, 0, 0, 0)
        self.textLayout.setSpacing(2)

        self.boxLayout.addWidget(self.iconWidget)
        self.boxLayout.addLayout(self.textLayout, 1)
        self.textLayout.addWidget(self.titleLabel, 0, Qt.AlignTop)
        self.textLayout.addWidget(self.contentLabel, 0, Qt.AlignTop)

    def enterEvent(self, event):
        self._isHover = True
        super().enterEvent(event)
        self.update()

    def leaveEvent(self, event):
        self._isHover = False
        super().leaveEvent(event)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        pc = 255 if isDarkTheme() else 0
        painter.setPen(QColor(pc, pc, pc, 24 if self._isHover else 12))
        if self._isHover:
            painter.setBrush(QColor(255, 255, 255, 21 if isDarkTheme() else 64))
        else:
            painter.setBrush(QColor(255, 255, 255, 13 if isDarkTheme() else 170))

        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 8, 8)


class SampleCardView(QWidget):
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.viewLayout: QVBoxLayout = QVBoxLayout(self)
        self.flowLayout: FlowLayout = FlowLayout()
        self.titleLabel: SubtitleLabel = SubtitleLabel(title, self)

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addLayout(self.flowLayout)
        self.viewLayout.setContentsMargins(36, 0, 0, 0)
        self.flowLayout.setContentsMargins(0, 0, 0, 24)

    def addSampleCard(self, icon: Union[str, QIcon, FluentIcon], title: str, content: str):
        self.flowLayout.addWidget(SampleCard(icon, title, content, self))