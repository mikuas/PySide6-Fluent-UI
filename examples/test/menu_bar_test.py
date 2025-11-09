# coding:utf-8
import sys
from typing import Union

from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QPoint, QRect, QSize, QTimer
from PySide6.QtGui import QAction, QIcon, Qt, QMouseEvent
from PySide6.QtWidgets import QMenuBar, QMenu, QGraphicsOpacityEffect, QWidget, QVBoxLayout, QComboBox, QPushButton, \
    QApplication

from PySide6FluentUI import FluentStyleSheet, FluentIcon


class AnimatedMenu(QMenu):
    def __init__(self, title="", parent=None):
        super().__init__(title, parent)
        self.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.Dialog  | Qt.FramelessWindowHint)

        FluentStyleSheet.MENU_BAR.apply(self)
        self.geometryAni: QPropertyAnimation = QPropertyAnimation(self, b"geometry", self)
        self.opacityEffect: QGraphicsOpacityEffect = QGraphicsOpacityEffect(self)
        self.opacityAni: QPropertyAnimation = QPropertyAnimation(self.opacityEffect, b"opacity", self)

        self.geometryAni.setDuration(200)
        self.opacityAni.setDuration(180)
        self.geometryAni.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.opacityAni.setEasingCurve(QEasingCurve.OutCubic)

        self.triggered.connect(self.hide)

    # def mousePressEvent(self, e: QMouseEvent):
    #     action = self.actionAt(e.position().toPoint())
    #     if action and not action.menu() and e.button() == Qt.MouseButton.LeftButton:
    #         self.fadeOut()
    #         self.hide()
    #     super().mousePressEvent(e)

    def showEvent(self, event):
        super().showEvent(event)
        # try:
        #     self.opacityAni.finished.disconnect(self.hide)
        # except (TypeError, RuntimeError): ...
        self.setGraphicsEffect(self.opacityEffect)
        size = self.sizeHint()
        startRect = QRect(self.pos(), QSize(size.width(), 0))

        self.geometryAni.setStartValue(startRect)
        self.geometryAni.setEndValue(QRect(self.pos(), size))
        self.opacityAni.setStartValue(0.0)
        self.opacityAni.setEndValue(1.0)

        self.setGeometry(startRect)
        self.opacityAni.start()
        self.geometryAni.start()

    def fadeOut(self):
        try:
            self.opacityAni.finished.disconnect(self.hide)
        except (TypeError, RuntimeError): ...
        self.opacityAni.setStartValue(1.0)
        self.opacityAni.setEndValue(0.0)
        self.opacityAni.start()
        self.opacityAni.finished.connect(self.hide)
    
    def exec(self, pos: Union[QPoint, None] = None):
        if pos:
            self.hide()
            self.move(pos)
        self.show()

    def exec_(self, pos: Union[QPoint, None] = None):
        self.exec(pos)


class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        FluentStyleSheet.MENU_BAR.apply(self)

    def enableTransparentBackground(self, enable: bool):
        self.setProperty("isTransparent", enable)
        # self.update()

    def createMenu(self, title: str) -> AnimatedMenu:
        return AnimatedMenu(title, self)


class Demo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RoundMenu 动画演示")
        self.resize(800, 520)

        self.menuBar: MenuBar = MenuBar(self)

        """ file menu """
        self.fileMenu = self.menuBar.createMenu("文件(&F)")
        self.fileMenu.addActions([
            QAction("新建标签页", self, icon=FluentIcon.HOME.icon(), shortcut="Ctrl+N", triggered=lambda: print("新建标签页")),
            QAction("新建窗口", self, icon=FluentIcon.GITHUB.icon(), shortcut="Ctrl+Shift+N", triggered=lambda: print("新建窗口")),
            QAction("新建Markdown选项卡", self, triggered=lambda: print("新建Markdown选项卡")),
            QAction("打开", self, shortcut="Ctrl+O", triggered=lambda: print("打开")),
        ])

        self.fileSubMenu = self.menuBar.createMenu("最近使用")
        self.fileSubMenu.addAction(QAction("没有最近使用的文件", self))
        self.fileMenu.addMenu(self.fileSubMenu)

        self.fileMenu.addActions([
            QAction("保存", self, icon=FluentIcon.SAVE.icon(), shortcut="Ctrl+S", triggered=lambda: print("保存")),
            QAction("另存为", self, shortcut="Ctrl+Shift+S", triggered=lambda: print("另存为")),
            QAction("全部保存", self, shortcut="Ctrl+Alt+S", triggered=lambda: print("全部保存")),
        ])
        self.fileMenu.addSeparator()

        self.fileMenu.addActions([
            QAction("页面设置", self, triggered=lambda: print("页面设置")),
            QAction("打印", self, shortcut="Ctrl+P", triggered=lambda: print("打印"))
        ])
        self.fileMenu.addSeparator()

        self.fileMenu.addActions([
            QAction("关闭选项卡", self, shortcut="Ctrl+W", triggered=lambda: print("关闭选项卡")),
            QAction("关闭窗口", self, shortcut="Ctrl+Shift+W", triggered=lambda: print("关闭窗口")),
            QAction("退出", self, shortcut="Ctrl+Q", triggered=QApplication.exit)
        ])

        """ edit menu """
        self.editMenu = self.menuBar.createMenu("编辑(&E)")
        self.editMenu.addAction(QAction("撤销", self, shortcut="Ctrl+Z", triggered=lambda: print("撤销")))
        self.editMenu.addSeparator()

        self.editMenu.addActions([
            QAction("剪切", self, icon=FluentIcon.CUT.icon(), shortcut="Ctrl+X", triggered=lambda: print("剪切")),
            QAction("复制", self, icon=FluentIcon.COPY.icon(), shortcut="Ctrl+C", triggered=lambda: print("复制")),
            QAction("粘贴", self, icon=FluentIcon.PASTE.icon(), shortcut="Ctrl+V", triggered=lambda: print("粘贴")),
            QAction("删除", self, icon=FluentIcon.DELETE.icon(), shortcut="Del", triggered=lambda: print("删除"))
        ])
        self.editMenu.addSeparator()

        self.editMenu.addActions([
            QAction("清除格式设置", self, triggered=lambda: print("清除格式设置")),
            QAction("使用必应搜索", self, triggered=lambda: print("使用必应搜索"))
        ])
        self.editMenu.addSeparator()

        self.editMenu.addActions([
            QAction("查找", self, shortcut="Ctrl+F", triggered=lambda: print("查找")),
            QAction("查找上一个", self, shortcut="F3", triggered=lambda: print("查找上一个")),
            QAction("查找下一个", self, shortcut="Shift+F3", triggered=lambda: print("查找下一个")),
            QAction("替换", self, shortcut="Ctrl+H", triggered=lambda: print("替换")),
            QAction("转到", self, shortcut="Ctrl+G", triggered=lambda: print("转到")),
        ])
        self.editMenu.addSeparator()

        self.editMenu.addActions([
            QAction("全选", self, shortcut="Ctrl+A", triggered=lambda: print("全选")),
            QAction("时间/日期", self, shortcut="F5", triggered=lambda: print("时间/日期")),
        ])
        self.editMenu.addSeparator()

        self.editMenu.addAction(QAction("字体", self, triggered=lambda: print("字体")))

        """ view menu """
        self.viewMenu = self.menuBar.createMenu("查看(&V)")
        self.zoomSubMenu = self.menuBar.createMenu("缩放")
        self.zoomSubMenu.addActions([
            QAction("放大", self, shortcut="Ctrl++", triggered=lambda: print("放大")),
            QAction("缩小", self, shortcut="Ctrl+-", triggered=lambda: print("缩小")),
            QAction("还原默认缩放", self, shortcut="Ctrl+R", triggered=lambda: print("还原默认缩放"))
        ])
        self.viewMenu.addMenu(self.zoomSubMenu)
        self.viewMenu.addActions([
            QAction("状态栏", self, triggered=lambda: print("状态栏"), checkable=True, checked=True),
            QAction("自动换行", self, triggered=lambda: print("自动换行"), checkable=True, checked=True),
        ])

        self.menuBar.addMenu(self.fileMenu)
        self.menuBar.addMenu(self.editMenu)
        self.menuBar.addMenu(self.viewMenu)

        layout = QVBoxLayout(self)
        layout.addWidget(self.menuBar, 0, Qt.AlignmentFlag.AlignTop)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        print('pre')

    def contextMenuEvent(self, event):
        super().contextMenuEvent(event)
        print("ContextMenuEvent")
        self.fileMenu.exec(event.globalPos())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    sys.exit(app.exec())
