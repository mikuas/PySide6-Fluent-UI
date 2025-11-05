# coding:utf-8
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMenuBar, QMenu, QGraphicsOpacityEffect
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, QParallelAnimationGroup
from PySide6.QtGui import QPainter, QAction


class AnimatedMenu(QMenu):
    """带WinUI弹出动画的QMenu"""
    def __init__(self, title="", parent=None):
        super().__init__(title, parent)
        self.aniGroup: QParallelAnimationGroup = QParallelAnimationGroup(self)

        self.__initOpacityEffect()
        self.__initAnimation()

        self.aniGroup.addAnimation(self.opacityAni)
        self.aniGroup.addAnimation(self.posAni)
        self.startPos = None
        self.endPos = None

        # Fluent样式
        self.setStyleSheet("""
            QMenu {
                background-color: #ffffff;
                border: 1px solid rgba(0,0,0,0.15);
                border-radius: 8px;
                padding: 6px;
                outline: none;
            }
            QMenu::item {
                padding: 6px 20px;
                border-radius: 4px;
                color: #1f1f1f;
            }
            QMenu::item:selected {
                background-color: rgba(0,120,215,0.12);
                color: #0067c0;
            }
        """)

    def __initOpacityEffect(self):
        self.opacityEffect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacityEffect)
        self.opacityEffect.setOpacity(0.0)

    def __initAnimation(self):
        self.opacityAni = QPropertyAnimation(self.opacityEffect, b"opacity", self)
        self.posAni = QPropertyAnimation(self, b"pos", self)

        self.opacityAni.setDuration(180)
        self.posAni.setDuration(180)
        self.opacityAni.setEasingCurve(QEasingCurve.OutCubic)
        self.posAni.setEasingCurve(QEasingCurve.OutCubic)

    def showEvent(self, event):
        super().showEvent(event)
        self.opacityAni.setStartValue(0.0)
        self.opacityAni.setEndValue(1.0)

        self.startPos = self.pos() - QPoint(0, 8)
        self.endPos = self.pos()

        self.posAni.setStartValue(self.startPos)
        self.posAni.setEndValue(self.endPos)

        self.aniGroup.start()


class WinUIMenuBar(QMenuBar):
    """WinUI风格菜单栏"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QMenuBar {
                background-color: #f3f3f3;
                padding: 4px 8px;
                font-family: "Segoe UI";
                font-size: 13px;
            }
            QMenuBar::item {
                padding: 6px 14px;
                margin: 2px;
                border-radius: 6px;
                color: #202020;
            }
            QMenuBar::item:selected {
                background-color: rgba(0,120,215,0.15);
                color: #0067c0;
            }
        """)

    def createMenu(self, title):
        return AnimatedMenu(title, self)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WinUI风格菜单栏 + 动画 + 快捷键 示例")
        self.resize(700, 400)

        menubar = WinUIMenuBar(self)
        self.setMenuBar(menubar)

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


if __name__ == "__main__":
    app = QApplication([])
    w = MainWindow()
    w.show()
    app.exec()
