# coding:utf-8
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPixmap, QLinearGradient, QColor, QFont
from PySide6.QtWidgets import QWidget, QVBoxLayout

from PySide6FluentUI import addRoundPath, FluentIcon, isDarkTheme, TitleLabel

from ..widgets.link_card_view import LinkCardView


class BannerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.viewLayout: QVBoxLayout = QVBoxLayout(self)
        self.pixmap: QPixmap = QPixmap(":/gallery/images/mm.webp")

        self.setFixedHeight(388)
        self.__initLinkCardView()

    def __initLinkCardView(self):
        self.titleLabel: TitleLabel = TitleLabel("PySide6-Fluent-UI Gallery", self)
        self.linkCardView: LinkCardView = LinkCardView(self)

        self.titleLabel.setFontSize(48, QFont.DemiBold)

        url = "https://github.com/mikuas/PySide6-Fluent-UI"

        self.linkCardView.addLinkCard(":/gallery/icons/app.ico", "Getting started", "An overview of app development options and samples.", url)
        self.linkCardView.addLinkCard(FluentIcon.GITHUB, "GitHub repo", "The latest fluent design controls and styles for your applications.",  url)
        self.linkCardView.addLinkCard(FluentIcon.CODE, "Code samples", "Find samples that demonstrate specific tasks, features and APIs.", url)
        self.linkCardView.addLinkCard(FluentIcon.FEEDBACK, "Send feedback", "Help us improve PySide6-Fluent-UI by providing feedback.", url)

        self.viewLayout.setContentsMargins(32, 8, 0, 0)
        self.viewLayout.addWidget(self.titleLabel, 0, Qt.AlignTop | Qt.AlignLeft)
        self.viewLayout.addWidget(self.linkCardView, 1, Qt.AlignBottom)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.LosslessImageRendering)
        painter.setPen(Qt.NoPen)

        rect = self.rect()

        painter.setClipPath(addRoundPath(rect, 12, 0, 0, 0))
        painter.drawPixmap(rect, self.pixmap)

        gradient = QLinearGradient(0, rect.height() // 2, 0, rect.height())
        c = 38 if isDarkTheme() else 248
        gradient.setColorAt(0, QColor(c, c, c, 64))
        gradient.setColorAt(1, QColor(c, c, c))

        painter.setBrush(gradient)
        painter.drawRect(rect)