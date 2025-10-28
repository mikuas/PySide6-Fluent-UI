# coding:utf-8
import sys
import subprocess
import os.path

from PySide6.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QFileDialog
from PySide6.QtGui import QImageReader
from PySide6.QtCore import Qt

from PySide6FluentUI import SplitWidget, DragFileWidget, SubtitleLabel, PushButton, PrimaryPushButton, \
    TransparentToolButton, FluentIcon, setToolTipInfo, ToolTipPosition, toggleTheme, InfoBar, InfoBarPosition, ComboBox

from .views.option_view import OptionView
from .views.preview_widget import PreviewWidget
from .utils.round_radius_utils import customRoundPixmap


class MainWindow(SplitWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 520)
        self.viewLayout: QVBoxLayout = QVBoxLayout(self)
        self.viewLayout.setContentsMargins(11, 38, 11, 11)
        self.image: str = ""
        self.imageTypes: list[str] = [f.data().decode() for f in QImageReader.supportedImageFormats()]

        print(self.imageTypes)

        self.fileFilter: str = "所有文件 (*.*);; "
        for f in self.imageTypes:
            self.fileFilter += f" {f}文件 (*.{f});;"

        self.titleLabel: SubtitleLabel = SubtitleLabel("圆角图片裁剪工具", self)
        self.fileWidget: DragFileWidget = DragFileWidget(
            fileFilter=self.fileFilter,
            isDashLine=True,
            parent=self
        )
        self.optionButton: PushButton = PushButton("设置圆角弧度", self)
        self.previewButton: PushButton = PushButton("预览", self)
        self.saveButton: PrimaryPushButton = PrimaryPushButton("保存", self)
        self.optionView: OptionView = OptionView(self.optionButton, self)
        self.saveTypeComboBox: ComboBox = ComboBox(self)
        self.previewWidget: PreviewWidget = PreviewWidget(self.previewButton, self)

        self.saveTypes: list[str] = ["png", "webp"]
        self.saveTypeComboBox.addItems(["png(体积大)", "webp(体积小)"])

        hBoxLayout = QHBoxLayout()
        self.viewLayout.addWidget(self.titleLabel, 0, Qt.AlignHCenter)
        self.viewLayout.addWidget(self.fileWidget, 1)

        self.viewLayout.addLayout(hBoxLayout)
        hBoxLayout.addWidget(self.optionButton)
        hBoxLayout.addWidget(self.previewButton)
        hBoxLayout.addWidget(self.saveTypeComboBox)
        hBoxLayout.addWidget(self.saveButton)

        self.toggleThemeButton: TransparentToolButton = TransparentToolButton(FluentIcon.CONSTRACT, self)
        self.toggleThemeButton.setFixedSize(46, 32)
        self.titleBar.hBoxLayout.insertWidget(4, self.toggleThemeButton)

        setToolTipInfo(self.toggleThemeButton, "切换主题", 2500, ToolTipPosition.TOP)
        self.connectSignalSlot()

    def getSuffixName(self, file: str):
        return file.split(".")[-1]

    def _updateImage(self, path):
        if bool(path):
            path = path[0]
            if self.getSuffixName(path) in self.imageTypes:
                self.image = path
                self.previewWidget.imageWidget.updateImage(path)

    def _updateRadius(self):
        self.previewWidget.imageWidget.updateRadius(*self.optionView.getRadius())

    def _onAppliButtonClicked(self):
        self._updateRadius()
        InfoBar.success(
            f"设置圆角成功! {self.optionView.getRadius()}",
            "",
            duration=3000,
            position=InfoBarPosition.TOP,
            parent=self
        )

    def _onSaveButtonClicked(self):
        if not self.image:
            InfoBar.error(
                "保存失败",
                "",
                duration=3000,
                isClosable=False,
                position=InfoBarPosition.TOP,
                parent=self
            )
            return
        savePath = os.path.dirname(self.image)
        openButton: TransparentToolButton = TransparentToolButton(FluentIcon.FOLDER, self)
        suffix = self.saveTypes[self.saveTypeComboBox.currentIndex()]
        saveDir = QFileDialog.getExistingDirectory(self, "选择保存文件夹", savePath)
        InfoBar.success(
            f"  保存成功! 文件路径: {saveDir}ClipResult.{suffix}  ",
            "",
            duration=-1,
            position=InfoBarPosition.TOP,
            parent=self
        ).addWidget(openButton)
        openButton.clicked.connect(lambda: subprocess.run(['explorer', os.path.normpath(saveDir)]))
        print(
            customRoundPixmap(self.image, *self.optionView.getRadius()).toImage().save(
                f"{saveDir}ClipResult.{suffix}", suffix
            )
        )

    def connectSignalSlot(self):
        self.optionButton.clicked.connect(self.optionView.show)
        self.previewButton.clicked.connect(self.previewWidget.show)
        self.fileWidget.draggedChange.connect(self._updateImage)
        self.fileWidget.selectionChange.connect(self._updateImage)
        self.optionView.applyButton.clicked.connect(self._onAppliButtonClicked)
        self.toggleThemeButton.clicked.connect(toggleTheme)
        self.saveButton.clicked.connect(self._onSaveButtonClicked)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
