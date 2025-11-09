from PySide6.QtWidgets import QApplication, QWidget, QMenu, QGraphicsOpacityEffect
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, QSize, QPoint
import sys



class AnimatedMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)

        # 高度动画
        self.geometryAni = QPropertyAnimation(self, b"geometry", self)
        self.geometryAni.setDuration(200)
        self.geometryAni.setEasingCurve(QEasingCurve.OutCubic)

        # 渐显动画
        self.opacityEffect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacityEffect)
        self.opacityAni = QPropertyAnimation(self.opacityEffect, b"opacity", self)
        self.opacityAni.setDuration(180)
        self.opacityAni.setEasingCurve(QEasingCurve.OutCubic)

        # 示例 actions
        self.addAction("选项 A")
        self.addAction("选项 B")
        self.addAction("选项 C")

    def showEvent(self, event):
        super().showEvent(event)
        size = self.sizeHint()
        startRect = QRect(self.pos(), QSize(size.width(), 0))

        self.geometryAni.setStartValue(startRect)
        self.geometryAni.setEndValue(QRect(self.pos(), size))
        self.opacityAni.setStartValue(0.0)
        self.opacityAni.setEndValue(1.0)

        self.setGeometry(startRect)
        self.geometryAni.start()
        self.opacityAni.start()

    def exec(self, pos=None):
        if pos:
            self.move(pos)
        self.show()  # show 会触发 showEvent 动画


class Demo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("右键菜单示例")
        self.resize(400, 300)

        self.menu = AnimatedMenu(self)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.menu.exec(event.globalPosition().toPoint())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec())
