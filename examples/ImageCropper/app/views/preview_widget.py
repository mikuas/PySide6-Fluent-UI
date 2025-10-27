# coding:utf-8
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QColor, QPixmap, QImage, QPainter, QPainterPath
from PySide6.QtCore import Qt, QSize, QRectF

from PySide6FluentUI import FlyoutDialog


class ImageWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.path: str = ""

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制路径（圆角矩形）
        path = QPainterPath()
        rect = QRectF(self.rect())
        path.addRoundedRect(rect, 0, 0)

        # 裁剪成圆角区域
        painter.setClipPath(path)

        # 绘制背景图片（自动缩放到窗口大小）
        painter.drawPixmap(self.rect(), QImage(self.path))

        # 可选：绘制边框
        painter.setPen(Qt.NoPen)
        painter.drawPath(path)


class PreviewWidget(FlyoutDialog):
    def __init__(self, target, parent=None):
        super().__init__(target, parent=parent)
        self.setMinimumSize(328, 328)
        self.viewLayout.setContentsMargins(3, 3, 3, 3)
        self.parent = parent

        self.imageWidget: ImageWidget = ImageWidget(self)
        self.viewLayout.addWidget(self.imageWidget, 1)