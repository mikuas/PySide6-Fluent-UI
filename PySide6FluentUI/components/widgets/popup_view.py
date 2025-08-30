# coding:utf-8
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGraphicsOpacityEffect
from PySide6.QtCore import Qt, QParallelAnimationGroup, QPropertyAnimation, QEasingCurve, QPoint
from PySide6.QtGui import QPainter, QPen, QColor

from ...common.style_sheet import isDarkTheme


class PopupView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.viewLayout: QVBoxLayout = QVBoxLayout(self)
        self.viewLayout.setSpacing(0)
        self.viewLayout.setContentsMargins(1, 1, 1, 1)

        self.aniGroup: QParallelAnimationGroup = QParallelAnimationGroup(self)
        self.opacity: QGraphicsOpacityEffect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity)
        self.setWindowOpacity(1)

        self.opacityAni: QPropertyAnimation = QPropertyAnimation(self.opacity, b'opacity', self)
        self.opacityAni.setDuration(300)
        self.opacityAni.setEasingCurve(QEasingCurve.OutQuad)

        self.posAni: QPropertyAnimation = QPropertyAnimation(self, b'pos')
        self.posAni.setDuration(200)
        self.posAni.setEasingCurve(QEasingCurve.Type.OutBack)

        self.aniGroup.addAnimation(self.opacityAni)
        self.aniGroup.addAnimation(self.posAni)

    def _run(self):
        self.opacityAni.setStartValue(0)
        self.opacityAni.setEndValue(1)
        self.posAni.setStartValue(self._slideStartPos())
        self.posAni.setEndValue(self._slideEndPos())
        self.aniGroup.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        if isDarkTheme():
            pc = 255
            bc = 32
        else:
            pc = 0
            bc = 244
        pen = QPen(QColor(pc, pc, pc, 32))
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        painter.setBrush(QColor(bc, bc, bc))

        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 6, 6)

    def _slideStartPos(self) -> QPoint:
        return self.__startPos

    def _slideEndPos(self) -> QPoint:
        return self.__endPos

    def _setPos(self, startPos: QPoint, endPos: QPoint):
        self.__startPos = startPos
        self.__endPos = endPos

    def exec(self, startPos: QPoint, endPos: QPoint):
        self._setPos(startPos, endPos)
        super().show()
        self.raise_()
        self._run()