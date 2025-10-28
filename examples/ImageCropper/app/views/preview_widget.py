# coding:utf-8
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtGui import QPixmap, QPainter, QPainterPath
from PySide6.QtCore import Qt

from PySide6FluentUI import FlyoutDialog, SubtitleLabel


class ImageWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.viewLayout: QVBoxLayout = QVBoxLayout(self)
        self.pixmap: QPixmap = QPixmap()
        self.sizeLabel: SubtitleLabel = SubtitleLabel("大小: 未知", self)
        self.sizeLabel.setFontSize(16)
        self.tl, self.tr, self.br, self.bl = 0, 0, 0, 0

        self.viewLayout.addWidget(self.sizeLabel, 1, Qt.AlignTop | Qt.AlignHCenter)

    def updateImage(self, path: str):
        self.pixmap = QPixmap(path)
        size = self.pixmap.size()
        self.sizeLabel.setText(f"大小: {size.width()}x{size.height()}")
        self.parent().setFixedSize(size.width() // 3, size.height() // 3 + 48)
        self.update()

    def updateRadius(self, tl: int, tr: int, br: int, bl: int):
        self.tl, self.tr, self.br, self.bl = tl, tr, br, bl
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

        rect = self.rect().adjusted(12, 48, -12, -12)
        path = QPainterPath()
        path.moveTo(rect.left() + self.tl, rect.top())
        path.lineTo(rect.right() - self.tr, rect.top())
        path.quadTo(rect.right(), rect.top(), rect.right(), rect.top() + self.tr)
        path.lineTo(rect.right(), rect.bottom() - self.br)
        path.quadTo(rect.right(), rect.bottom(), rect.right() - self.br, rect.bottom())
        path.lineTo(rect.left() + self.bl, rect.bottom())
        path.quadTo(rect.left(), rect.bottom(), rect.left(), rect.bottom() - self.bl)
        path.lineTo(rect.left(), rect.top() + self.tl)
        path.quadTo(rect.left(), rect.top(), rect.left() + self.tl, rect.top())

        painter.setClipPath(path)
        painter.drawPixmap(rect, self.pixmap)


class PreviewWidget(FlyoutDialog):
    def __init__(self, target, parent=None):
        super().__init__(target, parent=parent)
        self.viewLayout.setContentsMargins(3, 3, 3, 3)
        self.parent = parent

        self.imageWidget: ImageWidget = ImageWidget(self)
        self.viewLayout.addWidget(self.imageWidget, 1)