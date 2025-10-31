# coding:utf-8
from PySide6.QtWidgets import QWidget, QHBoxLayout
from PySide6.QtGui import QPixmap, QPainter, QPainterPath
from PySide6.QtCore import Qt

from PySide6FluentUI import FlyoutDialog, SubtitleLabel, TransparentToolButton, FluentIcon, setToolTipInfo, \
    ToolTipPosition


class ImageWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(256)
        self.viewLayout: QHBoxLayout = QHBoxLayout(self)
        self.pixmap: QPixmap = QPixmap()
        self.sizeLabel: SubtitleLabel = SubtitleLabel("大小: 未知", self)
        self.closeButton: TransparentToolButton = TransparentToolButton(FluentIcon.CLOSE, self)
        self.sizeLabel.setFontSize(16)
        self.tl, self.tr, self.br, self.bl = 0, 0, 0, 0

        self.viewLayout.addWidget(self.sizeLabel, 1, Qt.AlignTop | Qt.AlignHCenter)
        self.viewLayout.addWidget(self.closeButton, 0, Qt.AlignTop | Qt.AlignHCenter | Qt.AlignRight)

        setToolTipInfo(self.closeButton, "关闭", 2500, ToolTipPosition.TOP)

    def updateImage(self, path: str):
        self.pixmap = QPixmap(path)
        size = self.pixmap.size()
        w, h = size.width(), size.height()
        self.sizeLabel.setText(f"大小: {w}x{h}")

        if w - h > 128:
            scaled = (800, 520)
        elif h - w > 128:
            scaled = (480, 720)
        else:
            scaled = (600, 600)
        self.pixmap.scaled(*scaled, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.parent().setFixedSize(*scaled)
        self.update()

    def updateRadius(self, tl: int, tr: int, br: int, bl: int):
        self.tl, self.tr, self.br, self.bl = tl // 3, tr // 3, br // 3, bl // 3
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
        self.imageWidget: ImageWidget = ImageWidget(self)

        self.viewLayout.addWidget(self.imageWidget, 1)
        self.imageWidget.closeButton.clicked.connect(self.hide)
