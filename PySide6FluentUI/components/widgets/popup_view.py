# coding:utf-8
from PySide6.QtWidgets import QVBoxLayout, QGraphicsOpacityEffect, QFrame, QHBoxLayout, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, QParallelAnimationGroup, QPropertyAnimation, QEasingCurve, QPoint
from PySide6.QtGui import QPainter, QColor

from ...common.style_sheet import isDarkTheme


class ContainerFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        if isDarkTheme():
            pc, bc = 255, 39
        else:
            pc, bc = 0, 243
        painter.setPen(QColor(pc, pc, pc, 32))
        painter.setBrush(QColor(bc, bc, bc))
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 8, 8)


class FrameView(QFrame):

    def __init__(self, parent=None, layout=QVBoxLayout):
        super().__init__(parent)
        self.view: ContainerFrame = ContainerFrame(self)
        self.setLayout(QHBoxLayout())
        self.viewLayout: QVBoxLayout = layout(self.view)
        self.layout().addWidget(self.view)

        # add shadow
        self.__initShadowEffect()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)

    def __initShadowEffect(self):
        self.shadowEffect = QGraphicsDropShadowEffect(self)
        self.shadowEffect.setBlurRadius(25)
        self.shadowEffect.setColor(QColor(0, 0, 0, 60))
        self.shadowEffect.setOffset(0, 5)
        self.view.setGraphicsEffect(self.shadowEffect)


class PopupView(FrameView):
    def __init__(self, parent=None, layout=QVBoxLayout):
        super().__init__(parent, layout)
        self.viewLayout.setSpacing(0)
        self.viewLayout.setContentsMargins(1, 1, 1, 1)

        self.aniGroup: QParallelAnimationGroup = QParallelAnimationGroup(self)

        self.opacityAni: QPropertyAnimation = QPropertyAnimation(self, b'windowOpacity', self)
        self.opacityAni.setDuration(400)
        self.opacityAni.setEasingCurve(QEasingCurve.OutQuad)

        self.posAni: QPropertyAnimation = QPropertyAnimation(self, b'pos')
        self.posAni.setDuration(250)
        self.posAni.setEasingCurve(QEasingCurve.OutQuad)

        self.aniGroup.addAnimation(self.opacityAni)
        self.aniGroup.addAnimation(self.posAni)

    def showEvent(self, event):
        self.opacityAni.setStartValue(0)
        self.opacityAni.setEndValue(1)
        self.posAni.setStartValue(self._slideStartPos())
        self.posAni.setEndValue(self._slideEndPos())
        self.aniGroup.start()
        super().showEvent(event)

    def _slideStartPos(self) -> QPoint:
        return self.__startPos

    def _slideEndPos(self) -> QPoint:
        return self.__endPos

    def _setPos(self, startPos: QPoint, endPos: QPoint):
        self.__startPos = startPos
        self.__endPos = endPos

    def exec(self, startPos: QPoint, endPos: QPoint):
        self._setPos(startPos, endPos)
        self.raise_()
        super().show()