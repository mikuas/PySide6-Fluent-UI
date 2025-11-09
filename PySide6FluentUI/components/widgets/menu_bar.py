# coding:utf-8
from typing import Union

from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QPoint, Qt, QRect, QSize, QEvent
from PySide6.QtWidgets import QMenuBar, QMenu, QGraphicsOpacityEffect, QWidget, QApplication

from ...common.style_sheet import FluentStyleSheet


class AnimatedMenu(QMenu):
    def __init__(self, title="", parent: QWidget = None):
        super().__init__(title, parent)
        parent.window().installEventFilter(self)
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.WindowDoesNotAcceptFocus | Qt.Dialog)
        self.setFocusPolicy(Qt.NoFocus)
        FluentStyleSheet.MENU_BAR.apply(self)
        self.geometryAni: QPropertyAnimation = QPropertyAnimation(self, b"geometry", self)
        self.opacityAni: QPropertyAnimation = QPropertyAnimation(self)

        self.geometryAni.setDuration(200)
        self.geometryAni.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.opacityAni.setDuration(180)
        self.opacityAni.setEasingCurve(QEasingCurve.OutCubic)
        self.opacityAni.setPropertyName(b"opacity")

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
        self.opacityEffect: QGraphicsOpacityEffect = QGraphicsOpacityEffect(self)
        self.opacityAni.setTargetObject(self.opacityEffect)
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

    def eventFilter(self, watched, event):
        if event.type() in [QEvent.Type.MouseButtonPress, QEvent.Type.Move] and self.isVisible():
            self.hide()

        return super().eventFilter(watched, event)


class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        FluentStyleSheet.MENU_BAR.apply(self)

    def enableTransparentBackground(self, enable: bool):
        self.setProperty("isTransparent", enable)
        self.style().unpolish(self)
        self.style().polish(self)

    def createMenu(self, title: str) -> AnimatedMenu:
        return AnimatedMenu(title, self)