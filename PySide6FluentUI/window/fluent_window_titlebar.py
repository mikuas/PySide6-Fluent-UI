# coding:utf-8
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout

from ..common.style_sheet import FluentStyleSheet

from qframelesswindow import TitleBar, TitleBarBase


class FluentTitleBar(TitleBar):
    """ Fluent title bar"""

    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedHeight(48)
        self.hBoxLayout.removeWidget(self.minBtn)
        self.hBoxLayout.removeWidget(self.maxBtn)
        self.hBoxLayout.removeWidget(self.closeBtn)

        # add window icon
        self.iconLabel = QLabel(self)
        self.iconLabel.setFixedSize(18, 18)
        self.hBoxLayout.insertWidget(0, self.iconLabel, 0, Qt.AlignLeft | Qt.AlignVCenter)
        self.window().windowIconChanged.connect(self.setIcon)

        # add title label
        self.titleLabel = QLabel(self)
        self.hBoxLayout.insertWidget(1, self.titleLabel, 0, Qt.AlignLeft | Qt.AlignVCenter)
        self.titleLabel.setObjectName('titleLabel')
        self.window().windowTitleChanged.connect(self.setTitle)

        self.vBoxLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setSpacing(0)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonLayout.setAlignment(Qt.AlignTop)
        self.buttonLayout.addWidget(self.minBtn)
        self.buttonLayout.addWidget(self.maxBtn)
        self.buttonLayout.addWidget(self.closeBtn)
        self.vBoxLayout.addLayout(self.buttonLayout)
        self.vBoxLayout.addStretch(1)
        self.hBoxLayout.addLayout(self.vBoxLayout, 0)

        FluentStyleSheet.FLUENT_WINDOW.apply(self)

    def setTitle(self, title):
        self.titleLabel.setText(title)
        self.titleLabel.adjustSize()

    def setIcon(self, icon):
        self.iconLabel.setPixmap(QIcon(icon).pixmap(18, 18))


class MSFluentTitleBar(FluentTitleBar):

    def __init__(self, parent):
        super().__init__(parent)
        self.hBoxLayout.insertSpacing(0, 20)
        self.hBoxLayout.insertSpacing(2, 2)


class SplitTitleBar(TitleBar):

    def __init__(self, parent):
        super().__init__(parent)
        # add window icon
        self.iconLabel = QLabel(self)
        self.iconLabel.setFixedSize(18, 18)
        self.hBoxLayout.insertSpacing(0, 12)
        self.hBoxLayout.insertWidget(1, self.iconLabel, 0, Qt.AlignLeft | Qt.AlignBottom)
        self.window().windowIconChanged.connect(self.setIcon)

        # add title label
        self.titleLabel = QLabel(self)
        self.hBoxLayout.insertWidget(2, self.titleLabel, 0, Qt.AlignLeft | Qt.AlignBottom)
        self.titleLabel.setObjectName('titleLabel')
        self.window().windowTitleChanged.connect(self.setTitle)

        FluentStyleSheet.FLUENT_WINDOW.apply(self)

    def setTitle(self, title):
        self.titleLabel.setText(title)
        self.titleLabel.adjustSize()

    def setIcon(self, icon):
        self.iconLabel.setPixmap(QIcon(icon).pixmap(18, 18))


class CustomTitleBar(TitleBarBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(50)
        self.hBoxLayout = QHBoxLayout(self)
        self.iconLabel = QLabel(self)
        self.titleLabel = QLabel(self)

        self.titleLabel.setObjectName('titleLabel')
        self.iconLabel.setFixedSize(18, 18)

        # add buttons to layout
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.hBoxLayout.addSpacing(12)
        self.hBoxLayout.addWidget(self.iconLabel, 0, Qt.AlignLeft | Qt.AlignVCenter)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignLeft | Qt.AlignVCenter)

        self.initButton()
        self.window().windowIconChanged.connect(self.setIcon)
        self.window().windowTitleChanged.connect(self.setTitle)

        FluentStyleSheet.FLUENT_WINDOW.apply(self)

    def initButton(self):
        self.hBoxLayout.addStretch(1)

        self.hBoxLayout.addWidget(self.minBtn, 0, Qt.AlignRight | Qt.AlignTop)
        self.hBoxLayout.addWidget(self.maxBtn, 0, Qt.AlignRight | Qt.AlignTop)
        self.hBoxLayout.addWidget(self.closeBtn, 0, Qt.AlignRight | Qt.AlignTop)

    def setTitle(self, title):
        self.titleLabel.setText(title)
        self.titleLabel.adjustSize()

    def setIcon(self, icon):
        self.iconLabel.setPixmap(QIcon(icon).pixmap(18, 18))