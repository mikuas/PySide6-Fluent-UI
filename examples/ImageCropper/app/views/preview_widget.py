# coding:utf-8
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from PySide6.QtGui import QPixmap, QPainter, QPainterPath
from PySide6.QtCore import Qt

from PySide6FluentUI import FlyoutDialog, SubtitleLabel, TransparentToolButton, FluentIcon, setToolTipInfos, \
    ToolTipPosition


class ImageWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(256)
        self.viewLayout: QVBoxLayout = QVBoxLayout(self)
        self.pixmap: QPixmap = QPixmap()
        self.imageInfoLabel: SubtitleLabel = SubtitleLabel("图片: None 大小: None", self)
        self.closeButton: TransparentToolButton = TransparentToolButton(FluentIcon.CLOSE, self)
        self.imageInfoLabel.setFontSize(16)
        self.tl, self.tr, self.br, self.bl = 0, 0, 0, 0

        self.previousButton: TransparentToolButton = TransparentToolButton(FluentIcon.CARE_LEFT_SOLID, self)
        self.nextButton: TransparentToolButton = TransparentToolButton(FluentIcon.CARE_RIGHT_SOLID, self)

        titleLayout = QHBoxLayout()
        titleLayout.addWidget(self.imageInfoLabel, 1, Qt.AlignTop | Qt.AlignHCenter)
        titleLayout.addWidget(self.closeButton, 0, Qt.AlignTop | Qt.AlignHCenter | Qt.AlignRight)
        self.viewLayout.addLayout(titleLayout)

        self.previousButton.setVisible(False)
        self.previousButton.setFixedSize(35, 35)
        self.nextButton.setVisible(False)
        self.nextButton.setFixedSize(35, 35)

        setToolTipInfos([self.closeButton, self.previousButton, self.nextButton], ["关闭", "上一张", "下一张"], 2500, ToolTipPosition.TOP)

    def updateImage(self, path: str):
        self.pixmap = QPixmap(path)
        size = self.pixmap.size()
        w, h = size.width(), size.height()
        self.imageInfoLabel.setText(f"图片: {path.split("/")[-1]} 大小: {w}x{h}")

        if w - h > 128:
            scaled = (860, 600)
        elif h - w > 128:
            scaled = (495, 800)
        else:
            scaled = (650, 650)
        self.pixmap.scaled(*scaled, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.parent().setFixedSize(*scaled)
        self.update()

    def updateRadius(self, tl: int, tr: int, br: int, bl: int):
        self.tl, self.tr, self.br, self.bl = tl // 3, tr // 3, br // 3, bl // 3
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

        rect = self.rect().adjusted(12, self.imageInfoLabel.height() + 24, -12, -48)
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

    def enterEvent(self, event):
        self.previousButton.setVisible(True)
        self.nextButton.setVisible(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.previousButton.setVisible(False)
        self.nextButton.setVisible(False)
        super().leaveEvent(event)

    def resizeEvent(self, event):
        w, h = self.width(), self.height()
        self.previousButton.move(12, (h - 35) // 2)
        self.nextButton.move(w - 35 - 12, (h - 35) // 2)
        super().resizeEvent(event)


class PreviewWidget(FlyoutDialog):
    def __init__(self, target, parent=None):
        super().__init__(target, parent=parent)
        self.viewLayout.setContentsMargins(3, 3, 3, 3)
        self.imageWidget: ImageWidget = ImageWidget(self)

        self.viewLayout.addWidget(self.imageWidget, 1)
        self.imageWidget.closeButton.clicked.connect(self.hide)
