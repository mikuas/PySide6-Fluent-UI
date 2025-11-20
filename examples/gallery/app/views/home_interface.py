# coding:utf-8
from typing import Union

from PySide6.QtCore import Qt, QRect, QUrl
from PySide6.QtGui import QPainter, QPixmap, QPainterPath, QLinearGradient, QColor, QFont
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from PySide6FluentUI import SmoothScrollArea, addRoundPath, IconWidget, FluentIcon, SubtitleLabel, BodyLabel, \
    isDarkTheme, TitleLabel, CaptionLabel, FlowLayout

from ..utils.url_utils import openUrl


class JumpCard(QWidget):
    def __init__(self, icon: Union[str, FluentIcon], title: str, content: str, parent: QWidget = None):
        super().__init__(parent)
        self._isHover: bool = False
        self.iconWidget: IconWidget = IconWidget(icon, self)
        self.titleLabel: BodyLabel = BodyLabel(title, self)
        self.contentLabel: CaptionLabel = CaptionLabel(content, self)

        self.contentLabel.setWordWrap(True)
        self.iconWidget.setFixedSize(36, 36)
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
        if isDarkTheme():
            pc = 255
            bc = 32
        else:
            pc = 0
            bc = 255
        painter.setPen(QColor(pc, pc, pc, 24 if self._isHover else 16))
        if self._isHover:
            painter.setBrush(QColor(255, 255, 255, 21 if isDarkTheme() else 64))
        else:
            painter.setBrush(QColor(255, 255, 255, 13 if isDarkTheme() else 170))

        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 8, 8)


class LinkCark(JumpCard):
    def __init__(self, icon: Union[str, FluentIcon], title: str, content: str, url: Union[str, QUrl], parent: QWidget = None):
        super().__init__(icon, title, content, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.linkIconWidget: IconWidget = IconWidget(FluentIcon.LINK, self)
        self._url: Union[str, QUrl] = url

        self.iconWidget.setFixedSize(52, 52)
        self.titleLabel.setTextColor("black", "white")
        self.contentLabel.setTextColor("black", "white")
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

        self.__initCardWidget()

        self.basicInputSamplesTitle: SubtitleLabel = SubtitleLabel("基本输入", self)
        self.basicInputSamplesLayout: FlowLayout = FlowLayout()
        self.buttonButtonCard: JumpCard = JumpCard(FluentIcon.HOME, "按钮", "A control that responds to user input and emit clicked signal.")
        self.basicInputSamplesLayout.addWidget(self.buttonButtonCard)

        self.dateTimeSamplesTitle: SubtitleLabel = SubtitleLabel("日期时间", self)
        self.dateTimeSamplesLayout: FlowLayout = FlowLayout()

        self.viewLayout.setSpacing(32)
        self.viewLayout.addWidget(self.basicInputSamplesTitle)
        self.viewLayout.addLayout(self.basicInputSamplesLayout)

        self.viewLayout.addWidget(self.dateTimeSamplesTitle)

        self.viewLayout.addStretch(1)

    def __initCardWidget(self):
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
        w, h = self.width(), int(self.height() // 1.5)
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