# coding:utf-8
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QPropertyAnimation, Property
from PySide6.QtGui import QPainter, QPen, QColor
import sys


class LineWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._progress = 0.0  # 动画进度 (0 ~ 1)
        self.setMinimumSize(400, 200)
        self.animation = QPropertyAnimation(self, b"progress")
        self.animation.setDuration(300)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.start()

    def getProgress(self):
        return self._progress

    def setProgress(self, value):
        self._progress = value
        self.update()

    progress = Property(float, getProgress, setProgress)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen(QColor("#3498db"), 4)
        painter.setPen(pen)

        # 整条线的范围
        x1, x2 = 50, self.width() - 50
        y = self.height() // 2
        center = (x1 + x2) / 2

        # 根据 progress 计算当前半长度
        half_len = (x2 - x1) / 2 * self._progress
        if half_len > 0:
            # 从中间往两边画
            painter.drawLine(center - half_len, y, center + half_len, y)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = LineWidget()
    w.show()
    sys.exit(app.exec())
