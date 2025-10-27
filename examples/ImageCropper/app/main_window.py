# coding:utf-8
import sys
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QPixmap, QPainter, QPainterPath
from PySide6.QtCore import Qt, QRectF

from PySide6FluentUI import SplitWidget, DragFileWidget, SubtitleLabel, ImageLabel, PushButton, PrimaryPushButton

from examples.ImageCropper.app.views.option_view import OptionView
from examples.ImageCropper.app.views.preview_widget import PreviewWidget


class MainWindow(SplitWidget):
    def __init__(self):
        super().__init__()
        self.viewLayout: QVBoxLayout = QVBoxLayout(self)
        self.viewLayout.setContentsMargins(11, 38, 11, 11)
        self.imagePath: str = ""

        self.titleLabel: SubtitleLabel = SubtitleLabel("圆角图片制作工具", self)
        self.fileWidget: DragFileWidget = DragFileWidget(fileFilter="", isDashLine=True, parent=self)
        self.optionButton: PushButton = PushButton("选项", self)
        self.previewButton: PushButton = PushButton("预览", self)
        self.saveButton: PrimaryPushButton = PrimaryPushButton("保存", self)
        self.optionView: OptionView = OptionView(self.optionButton, self)
        self.previewWidget: PreviewWidget = PreviewWidget(self.previewButton, self)

        hBoxLayout = QHBoxLayout()
        self.viewLayout.addWidget(self.titleLabel, 0, Qt.AlignLeft)
        self.viewLayout.addWidget(self.fileWidget, 1)

        self.viewLayout.addLayout(hBoxLayout)
        hBoxLayout.addWidget(self.optionButton)
        hBoxLayout.addWidget(self.previewButton)
        hBoxLayout.addWidget(self.saveButton)

        self.connectSignalSlot()

    def updateImage(self, path: str):
        if type(path) is list:
            path = path[0]
        self.imagePath = path
        self.previewWidget.imageWidget.path = path
        self.previewWidget.imageWidget.update()

    def connectSignalSlot(self):
        self.optionButton.clicked.connect(self.optionView.show)
        self.previewButton.clicked.connect(self.previewWidget.show)
        self.fileWidget.draggedChange.connect(self.updateImage)
        self.fileWidget.selectionChange.connect(self.updateImage)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # label = QLabel()
    # # 分别是左上、右上、右下、左下
    # pixmap = rounded_pixmap_custom("IMG_20251004_155527.jpg", 80, 40, 10, 0)
    # label.setPixmap(pixmap)
    # pixmap.save("rounded_custom.png", "PNG")
    # label.show()

    sys.exit(app.exec())
