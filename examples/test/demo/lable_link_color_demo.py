# coding:utf-8
import re
import sys
from typing import Union

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextBrowser
from PySide6.QtGui import QColor, QPalette
from PySide6.QtCore import Qt

from PySide6FluentUI import SubtitleLabel, RoundMenu, Action, FluentIcon
from PySide6FluentUI.common.overload import singledispatchmethod


class LinkLabel(QLabel):

    @singledispatchmethod
    def __init__(self, parent=None):
        super().__init__(parent)
        self._postInit()

    @__init__.register
    def _(self, text: str, parent: QWidget = None):
        super().__init__(text, parent)
        self._postInit()

    def _postInit(self):
        self.setOpenExternalLinks(True)
        self.copyMenu: RoundMenu = RoundMenu(parent=self)
        self.copyMenu.addAction(Action(FluentIcon.COPY, "复制链接地址", self, triggered=self.copyLink))

    def copyLink(self):
        QApplication.clipboard().setText(self.getLink())

    def getLink(self) -> Union[str, None]:
        return re.search(r"href=['\"](.*?)['\"]", self.text()).group(1)

    def contextMenuEvent(self, event):
        event.accept()
        self.copyMenu.exec(event.globalPos())


class LabelLinkColorDemoInterface(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.viewLayout: QVBoxLayout = QVBoxLayout(self)

        # self.linkLabel: LinkLabel = LinkLabel(self)
        self.linkLabel: LinkLabel = LinkLabel("访问我的<a href='https://www.bilibili.com' style='color: deeppink; text-decoration: none;'>主页</a>", self)
        self.linkLabel.setOpenExternalLinks(True)

        self.viewLayout.addWidget(self.linkLabel, 0, Qt.AlignCenter)


def main():
    app = QApplication(sys.argv)
    window = LabelLinkColorDemoInterface()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()