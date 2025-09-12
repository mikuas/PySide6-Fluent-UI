# coding:utf-8
from enum import Enum

from PySide6FluentUI import FluentIconBase, IconWidget, Theme, FluentIcon


class FIF(FluentIconBase, Enum):

    ColorPicker = "color-picker"
    B = "anquanbaozhang"
    C = "bofangjilu"
    D = "color-picker"
    E = "dianzan"
    F = "dingwei"
    G = "ditu"
    H = "jubao"
    J = "shangchuantupian"
    K = "tijiaoyanzi"
    L = "skip-forward-fill"
    I = "skip-backward"
    M = "skip-forward"
    N = "skip-backward-fill"
    O = "rewind"
    P = "fast-forward"


    def path(self, theme=Theme.AUTO):
        return f"C:/Users/Administrator/Downloads/Png/{self.value}.svg"


import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt


class Window(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setLayout(QHBoxLayout())

        self.iw = IconWidget(self)
        self.iw.setFixedSize(26, 26)
        self.iw.setIcon(FIF.P.colored(QColor("red"), QColor("red")))

        self.layout().addWidget(self.iw)

# <file>images/icons/SkipEnd_white.svg</file>
# <file>images/icons/SkipEndFill_white.svg</file>
# <file>images/icons/SkipStart_white.svg</file>
# <file>images/icons/SkipStartFill_white.svg</file>
# <file>images/icons/SkipEnd_black.svg</file>
# <file>images/icons/SkipEndFill_black.svg</file>
# <file>images/icons/SkipStart_black.svg</file>
# <file>images/icons/SkipStartFill_black.svg</file>
# <file>images/icons/SkipBackward_black.svg</file>
# <file>images/icons/SkipBackwardFill_black.svg</file>
# <file>images/icons/SkipForwardV_black.svg</file>
# <file>images/icons/SkipForwardVFill_black.svg</file>
# <file>images/icons/SkipBackward_white.svg</file>
# <file>images/icons/SkipBackwardFill_white.svg</file>
# <file>images/icons/SkipForwardV_white.svg</file>
# <file>images/icons/SkipForwardVFill_white.svg</file>


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())

    ...

if __name__ == '__main__':
    main()