# coding:utf-8
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QMainWindow
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

        menubar = MenuBar(self)
        self.viewLayout.addWidget(menubar, 0, Qt.AlignTop)

        self.connectSignalSlot()

        # ===== 文件菜单 =====
        file_menu = menubar.createMenu("文件")

        act_new = QAction("新建", self)
        act_new.setShortcut("Ctrl+N")

        act_open = QAction("打开", self)
        act_open.setShortcut("Ctrl+O")

        act_exit = QAction("退出", self)
        act_exit.setShortcut("Alt+F4")
        act_exit.triggered.connect(self.close)

        file_menu.addAction(act_new)
        file_menu.addAction(act_open)
        file_menu.addSeparator()
        file_menu.addAction(act_exit)
        menubar.addMenu(file_menu)

        # ===== 编辑菜单 =====
        edit_menu = menubar.createMenu("编辑")

        act_copy = QAction("复制", self)
        act_copy.setShortcut("Ctrl+C")

        act_paste = QAction("粘贴", self)
        act_paste.setShortcut("Ctrl+V")

        act_cut = QAction("剪切", self)
        act_cut.setShortcut("Ctrl+X")

        edit_menu.addAction(act_copy)
        edit_menu.addAction(act_paste)
        edit_menu.addAction(act_cut)
        menubar.addMenu(edit_menu)

        # ===== 帮助菜单 =====
        help_menu = menubar.createMenu("帮助")
        act_about = QAction("关于", self)
        act_about.setShortcut("F1")
        help_menu.addAction(act_about)

        self.toggleButton: ToggleButton = ToggleButton("Toggle", self)
        self.viewLayout.addWidget(self.toggleButton)

        self.toggleButton.toggled.connect(
            lambda checked: {
                print(checked), menubar.enableTransparentBackground(checked)
            }
        )


if __name__ == "__main__":
    app = QApplication([])
    w = MainWindow()
    w.show()
    app.exec()