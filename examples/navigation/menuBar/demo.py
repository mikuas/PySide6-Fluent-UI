# coding:utf-8
import sys
from typing import List

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QMainWindow, QMenu
from PySide6.QtGui import QColor, QAction
from PySide6.QtCore import Qt

from PySide6FluentUI import MenuBar, ToggleButton
from examples.window.splitWidget.demo import Interface


class MainWindow(Interface):
    def __init__(self):
        super().__init__()
        self.resize(800, 520)
        self.viewLayout: QVBoxLayout = QVBoxLayout(self)
        self.viewLayout.setContentsMargins(12, 35, 12, 12)

        self.menuBar: MenuBar = MenuBar(self)
        self.toggleButton: ToggleButton = ToggleButton("Toggle", self)

        self.createSubMenu(
            "文件(&F)", 11, 6, 11, "历史文件", ["Ctrl", ["A", "B", "C", "D", "E", "", "F", "G", "H", "J"]]
        ).createSubMenu(
            "编辑(&E)", 16, 8, 16, "编辑历史", ["Shift", ["A", "B", "C", "D", "E", "F", "G", "", "H", "J", "K", "L", "M", "N", "O"]]
        ).createSubMenu(
            "视图(&V)", 25, 12, 11, "放大倍率", ["Ctrl+Shift", ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', '', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W']]
        ).createSubMenu(
            "选项(&O)", 7, 3, 7, "子选项", ["Ctrl+Alt", ["A", "B", "", "C", "D", "E"]]
        ).createSubMenu(
            "保存(&S)", 5, 2, 5, "另存为", ["Ctrl+Alt+Shift", ["A", "", "B",  "C", "D"]]
        )

        self.viewLayout.addWidget(self.menuBar, 0, Qt.AlignTop)
        self.viewLayout.addWidget(self.toggleButton)
        self.connectSignalSlot()

        self.toggleButton.toggled.connect(
            lambda checked: {
                print(checked), self.menuBar.enableTransparentBackground(checked)
            }
        )

    def createSubMenu(self, title: str, rg: int, expandIndex: int, subRg: int, subTitle: str, shortcut: list[
        str, list[str]]):
        menu = self.menuBar.createMenu(title)
        title = title.split("(")[0]
        for i in range(1, rg):
            if i == expandIndex:
                subMenu = self.menuBar.createMenu(subTitle)
                for _ in range(1, subRg):
                    action = QAction(f"Sub Item {subTitle} {_}", self)
                    subMenu.addAction(action)
                menu.addMenu(subMenu)
                menu.addSeparator()
                continue
            action = QAction(f"Item {title} {i}", self, shortcut=f"{shortcut[0]}+{shortcut[1][i - 1]}")
            # action.setShortcut(f"{shortcut[0]}+{shortcut[1][i - 1]}")
            menu.addAction(action)
        self.menuBar.addMenu(menu)
        return self


if __name__ == "__main__":
    app = QApplication([])
    w = MainWindow()
    w.show()
    app.exec()