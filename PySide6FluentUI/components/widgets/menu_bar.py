# coding:utf-8
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QPoint
from PySide6.QtWidgets import QMenuBar, QMenu, QGraphicsOpacityEffect

from ...common.style_sheet import FluentStyleSheet


class AnimatedMenu(QMenu):
    def __init__(self, title="", parent=None):
        super().__init__(title, parent)
        FluentStyleSheet.MENU_BAR.apply(self)

    def __createAni(self):
        self.opacityEffect: QGraphicsOpacityEffect = QGraphicsOpacityEffect(self)
        self.opacityAni: QPropertyAnimation = QPropertyAnimation(self.opacityEffect, b"opacity", self)
        self.posAni: QPropertyAnimation = QPropertyAnimation(self, b"pos", self)

        self.opacityAni.setDuration(180)
        self.opacityAni.setEasingCurve(QEasingCurve.OutCubic)
        self.posAni.setDuration(180)
        self.posAni.setEasingCurve(QEasingCurve.OutCubic)

        self.setGraphicsEffect(self.opacityEffect)
        self.opacityEffect.setOpacity(0.0)

        self.opacityAni.setStartValue(0.0)
        self.opacityAni.setEndValue(1.0)
        self.posAni.setStartValue(self.pos() - QPoint(0, 8))
        self.posAni.setEndValue(self.pos())

        self.opacityAni.start()
        self.posAni.start()

    def showEvent(self, event):
        super().showEvent(event)
        self.__createAni()


class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        FluentStyleSheet.MENU_BAR.apply(self)

    def enableTransparentBackground(self, enable: bool):
        self.setProperty("isTransparent", enable)

    def createMenu(self, title: str) -> AnimatedMenu:
        return AnimatedMenu(title, self)