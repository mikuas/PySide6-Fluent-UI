# coding:utf-8
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt


from PySide6FluentUI import PrimarySplitPushButton, FluentIcon, InfoBar, InfoBarPosition, RoundMenu, Action


# from qfluentwidgets import PrimarySplitPushButton, FluentIcon, RoundMenu, Action, InfoBar, InfoBarPosition


class Window(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setLayout(QVBoxLayout())

        self.button: PrimarySplitPushButton = PrimarySplitPushButton(FluentIcon.ACCEPT, "Clicked", self)
        self.layout().addWidget(self.button)
        print(self.button.styleSheet())

        menu = RoundMenu(parent=self.button)
        menu.addAction(Action(FluentIcon.BASKETBALL, 'Basketball', triggered=lambda: print("你干嘛~")))
        menu.addAction(Action(FluentIcon.ALBUM, 'Sing', triggered=lambda: print("喜欢唱跳RAP")))
        menu.addAction(Action(FluentIcon.MUSIC, 'Music', triggered=lambda: print("只因你太美")))

        # 添加菜单
        self.button.setFlyout(menu)

        self.button.clicked.connect(
            lambda: {
                InfoBar.success(
                    "Lecuss",
                    "Content",
                    position=InfoBarPosition.TOP, parent=self
                )
            }
        )


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())



if __name__ == '__main__':
    main()