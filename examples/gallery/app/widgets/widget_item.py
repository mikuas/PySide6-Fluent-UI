# coding:utf-8
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor, QDesktopServices, QFont

from PySide6FluentUI import SubtitleLabel, BodyLabel, FluentIcon, IconWidget, isDarkTheme, setFont, drawRoundRect


class WidgetCard(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        if isDarkTheme():
            pc = 255
            bc = 0
            a = 32
        else:
            pc = 0
            bc = 243
            a = 170
        painter.setPen(QColor(pc, pc, pc, 16))
        painter.setBrush(QColor(bc, bc, bc, a))
        drawRoundRect(painter, self.rect(), 10, 10, 0, 0)


class CodeLinkCard(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.isHover: bool = False
        self.setFixedHeight(57)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def enterEvent(self, event):
        self.isHover = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.isHover = False
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        if isDarkTheme():
            pc = 255
            bc = 52
            a = 64
        else:
            pc = 0
            bc = 255
            a = 170
        painter.setPen(QColor(pc, pc, pc, 16))
        painter.setBrush(QColor(bc, bc, bc, a))
        painter.setOpacity(0.678 if self.isHover else 1)
        drawRoundRect(painter, self.rect(), 0, 0, 10, 10)

    def mouseReleaseEvent(self, event):
        QDesktopServices.openUrl("https://github.com/mikuas/PySide6-Fluent-UI.git")
        super().mouseReleaseEvent(event)


class ItemCard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(114)
        self.widgetCard: WidgetCard = WidgetCard(self)
        self.codeLinkCard: CodeLinkCard = CodeLinkCard(self)
        self.vBoxLayout: QVBoxLayout = QVBoxLayout(self)

        self.widgetLayout: QHBoxLayout = QHBoxLayout(self.widgetCard)
        self.codeLinkLayout: QHBoxLayout = QHBoxLayout(self.codeLinkCard)

        self.title: BodyLabel = BodyLabel("源代码", self)
        self.iconWidget: IconWidget = IconWidget(FluentIcon.LINK, self)
        self.iconWidget.setFixedSize(16, 16)

        self.__initLayout()

    def __initLayout(self):
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.vBoxLayout.addWidget(self.widgetCard, 1)
        self.vBoxLayout.addWidget(self.codeLinkCard, 0)

        self.widgetLayout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.widgetLayout.setSpacing(12)
        self.widgetLayout.setContentsMargins(15, 0, 15, 0)

        self.codeLinkLayout.setContentsMargins(22, 0, 22, 0)
        self.codeLinkLayout.addWidget(self.title, 0, Qt.AlignLeft | Qt.AlignVCenter)
        self.codeLinkLayout.addWidget(self.iconWidget, 1, Qt.AlignRight | Qt.AlignVCenter)


class StandardItem(QWidget):
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.vBoxLayout: QVBoxLayout = QVBoxLayout(self)

        self.title: SubtitleLabel = SubtitleLabel(title, self)
        self.card: ItemCard = ItemCard(self)

        self.vBoxLayout.addWidget(self.title)
        self.vBoxLayout.addWidget(self.card, 1)
        self.vBoxLayout.addStretch(1)

        setFont(self.title, 16, QFont.DemiBold)

    def addWidget(self, widget: QWidget, stretch=0, alignment=Qt.AlignLeft | Qt.AlignVCenter) -> None:
        self.card.widgetLayout.addWidget(widget, stretch, alignment)
    
    def addLayout(self, layout: QLayout, stretch=0) -> None:
        self.card.widgetLayout.addLayout(layout, stretch)