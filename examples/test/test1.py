from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QGraphicsOpacityEffect, QMenu
)
from PySide6.QtCore import (
    Qt, QRect, QPropertyAnimation, QParallelAnimationGroup, QEasingCurve, QPoint
)
import sys


class DropDownMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(256, 328)

        # 初始透明度
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0.0)

    def paintEvent(self, event):
        # super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        painter.setPen(QColor(0, 0, 0, 32))
        painter.setBrush(QColor(255, 255, 255))
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 8, 8)
        painter.setPen(QColor(0, 0, 0))
        painter.drawText(self.rect(), Qt.AlignCenter, "Hello World")

    def exec(self, pos: QPoint):
        self.geo = QRect(pos, self.size())
        if self.isVisible():
            self.hide()
        self.show()

    def showEvent(self, event):
        print('show')
        # 菜单从按钮正下方展开（高度从 0 → h）
        start_geo = QRect(self.geo.x(), self.geo.y(), self.width(), 0)

        anim_geo = QPropertyAnimation(self, b"geometry")
        anim_geo.setDuration(150)
        anim_geo.setStartValue(start_geo)
        anim_geo.setEndValue(self.geo)
        anim_geo.setEasingCurve(QEasingCurve.Type.OutQuad)  # 平滑展开

        # 透明度动画
        anim_opacity = QPropertyAnimation(self.opacity_effect, b"opacity")
        anim_opacity.setDuration(150)
        anim_opacity.setStartValue(0.0)
        anim_opacity.setEndValue(1.0)
        anim_opacity.setEasingCurve(QEasingCurve.OutQuad)

        # 并行动画
        group = QParallelAnimationGroup(self)
        group.addAnimation(anim_geo)
        group.addAnimation(anim_opacity)

        super().showEvent(event)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.menu = DropDownMenu(self)

    def contextMenuEvent(self, event):
        self.menu.exec(event.globalPos())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.resize(400, 300)
    w.show()
    sys.exit(app.exec())
