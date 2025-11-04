# coding:utf-8
from typing import Union

from PySide6.QtCore import Qt, QRect, QUrl
from PySide6.QtGui import QPainter, QPixmap, QPainterPath, QLinearGradient, QColor, QFont
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from PySide6FluentUI import SmoothScrollArea, addRoundPath, IconWidget, FluentIcon, SubtitleLabel, BodyLabel, \
    isDarkTheme, TitleLabel

from ..utils.url_utils import openUrl


class LinkCark(QWidget):
    def __init__(self, icon: Union[str, FluentIcon], title: str, content: str, url: Union[str, QUrl], parent: QWidget = None):
        super().__init__(parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._isHover: bool = False
        self._url: Union[str, QUrl] = url
        self.boxLayout: QVBoxLayout = QVBoxLayout(self)

        self.iconWidget: IconWidget = IconWidget(icon, self)
        self.titleLabel: SubtitleLabel = SubtitleLabel(title, self)
        self.contentLabel: BodyLabel = BodyLabel(content, self)
        self.linkIconWidget: IconWidget = IconWidget(FluentIcon.LINK, self)

        self.iconWidget.setFixedSize(52, 52)
        self.contentLabel.setWordWrap(True)
        self.titleLabel.setTextColor("black", "white")
        self.contentLabel.setTextColor("black", "white")
        self.linkIconWidget.setFixedSize(18, 18)

        self.__initLayout()
        self.setFixedSize(200, 234)

    def __initLayout(self):
        self.boxLayout.setContentsMargins(26, 26, 16, 16)
        self.boxLayout.addWidget(self.iconWidget, 0, Qt.AlignLeft | Qt.AlignTop)
        self.boxLayout.addWidget(self.titleLabel)
        self.boxLayout.addWidget(self.contentLabel)
        self.boxLayout.addWidget(self.linkIconWidget, 0, Qt.AlignBottom | Qt.AlignRight)

    def mouseReleaseEvent(self, event):
        openUrl(self._url)
        super().mouseReleaseEvent(event)

    def enterEvent(self, event):
        self._setIsHover(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._setIsHover(False)
        super().leaveEvent(event)

    def _setIsHover(self, isHover: bool):
        if isHover == self._isHover:
            return
        self._isHover = isHover
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if isDarkTheme():
            pc = 255
            c = 39
        else:
            pc = 39
            c = 255
        painter.setPen(QColor(pc, pc, pc, 32))
        painter.setBrush(QColor(c, c, c, 186 if self._isHover else 211))
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 8, 8)


class HomeInterface(SmoothScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("HomeInterface")
        self.__initScrollArea()
        # self.image = ImageLabel(str(Path(__file__).resolve().parents[2] / "resources" / "images" / "ATRI.jpg"), self)
        self.pixmap: QPixmap = QPixmap(":/gallery/images/mm.webp")
        self.linkLayout: QHBoxLayout = QHBoxLayout()

        self.__initWidget()
        self.viewLayout.addStretch(1)

    def __initWidget(self):
        self.titleLabel: TitleLabel = TitleLabel("PySide6-Fluent-UI Gallery", self)
        self.titleLabel.setFontSize(48, QFont.DemiBold)
        self.__initLayout()

        url = "https://github.com/mikuas/PySide6-Fluent-UI"

        self.addLindCard(":/gallery/icons/app.ico", "Getting started", "An overview of app development options and samples.", url, self)
        self.addLindCard(FluentIcon.GITHUB, "GitHub repo", "The latest fluent design controls and styles for your applications.",  url, self)
        self.addLindCard(FluentIcon.CODE, "Code samples", "Find samples that demonstrate specific tasks, features and APIs.", url, self)
        self.addLindCard(FluentIcon.FEEDBACK, "Send feedback", "Help us improve PySide6-Fluent-UI by providing feedback.", url, self)

    def __initLayout(self):
        self.linkLayout.setAlignment(Qt.AlignLeft)
        self.linkLayout.setSpacing(16)

        self.viewLayout.addWidget(self.titleLabel, 0, Qt.AlignLeft)
        self.viewLayout.setContentsMargins(36, 48, 8, 8)
        self.viewLayout.addSpacing(74)
        self.viewLayout.addLayout(self.linkLayout)

    def addLindCard(self, icon: Union[str, FluentIcon], title: str, content: str, url: Union[str, QUrl], parent: QWidget = None):
        linkCard = LinkCark(icon, title, content, url, parent)
        self.linkLayout.addWidget(linkCard)

    def __initScrollArea(self):
        self._widget: QWidget = QWidget()
        self.viewLayout: QVBoxLayout = QVBoxLayout(self._widget)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidget(self._widget)
        self.setWidgetResizable(True)
        self.enableTransparentBackground()

    def paintEvent(self, e):
        painter = QPainter(self.viewport())
        painter.setRenderHints(QPainter.Antialiasing | QPainter.LosslessImageRendering)
        painter.setPen(Qt.NoPen)
        w, h = self.width(), 446
        rect = QRect(0, 0, w, h)

        painter.setClipPath(addRoundPath(rect, 12, 0, 0, 0))
        painter.drawPixmap(rect, self.pixmap)

        gradient = QLinearGradient(0, 64, 0, h)
        c = 39 if isDarkTheme() else 255
        gradient.setColorAt(0, QColor(c, c, c, 0))
        gradient.setColorAt(1, QColor(c, c, c, 234))

        painter.setBrush(gradient)
        painter.drawRect(0, 0, w, h)


def main():
    import sys
    import examples.gallery.resources.gallery_resources
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = HomeInterface()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()