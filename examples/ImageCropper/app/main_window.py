# coding:utf-8
import sys
import subprocess
import os.path

from PySide6.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QFileDialog
from PySide6.QtGui import QImageReader
from PySide6.QtCore import Qt

from PySide6FluentUI import SplitWidget, DragFileWidget, SubtitleLabel, PushButton, PrimaryPushButton, \
    TransparentToolButton, FluentIcon, setToolTipInfo, ToolTipPosition, toggleTheme, InfoBar, InfoBarPosition, ComboBox, \
    SwitchButton

from .views.option_view import OptionView
from .views.preview_widget import PreviewWidget
from .utils.round_radius_utils import customRoundPixmap
from .common.config import cfg


class MainWindow(SplitWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 520)
        self.viewLayout: QVBoxLayout = QVBoxLayout(self)
        self.viewLayout.setContentsMargins(11, 38, 11, 11)
        self.image: str = ""
        self.saveDir: str = cfg.saveDir.value
        self.imageTypes: list[str] = [f.data().decode() for f in QImageReader.supportedImageFormats()]

        print(self.imageTypes)

        self.fileFilter: str = "所有文件 (*.*);; "
        for f in self.imageTypes:
            self.fileFilter += f" {f}文件 (*.{f});;"

        self.titleLabel: SubtitleLabel = SubtitleLabel("圆角图片裁剪工具", self)
        self.memorySavePathSwitchButton: SwitchButton = SwitchButton(self)
        self.memorySavePathSwitchButton.setChecked(cfg.isMemorySavePath.value)
        self.fileWidget: DragFileWidget = DragFileWidget(
            fileFilter=self.fileFilter,
            isDashLine=True,
            parent=self
        )
        self.fileWidget.setLabelText("拖动图像文件到此")

        self.optionButton: PushButton = PushButton("设置圆角弧度", self)
        self.previewButton: PushButton = PushButton("预览", self)
        self.saveButton: PrimaryPushButton = PrimaryPushButton("保存", self)
        self.optionView: OptionView = OptionView(self.optionButton, self)
        self.saveTypeComboBox: ComboBox = ComboBox(self)
        self.previewWidget: PreviewWidget = PreviewWidget(self.previewButton, self)

        self.saveTypes: list[str] = ["png", "webp"]
        self.saveTypeComboBox.addItems(["png(体积大)", "webp(体积小)"])

        titleLayout = QHBoxLayout()
        self.viewLayout.addLayout(titleLayout)
        titleLayout.addWidget(self.titleLabel, 0, Qt.AlignLeft)
        titleLayout.addWidget(self.memorySavePathSwitchButton, 0, Qt.AlignRight)
        self.memorySavePathSwitchButton.setEnabled(cfg.isMemorySavePath.value)
        self.memorySavePathSwitchButton.setOffText("记忆保存位置(关闭)")
        self.memorySavePathSwitchButton.setOnText("记忆保存位置(开启)")

        self.viewLayout.addWidget(self.fileWidget, 1)

        buttonLayout = QHBoxLayout()
        self.viewLayout.addLayout(buttonLayout)
        buttonLayout.addWidget(self.optionButton)
        buttonLayout.addWidget(self.previewButton)
        buttonLayout.addWidget(self.saveTypeComboBox)
        buttonLayout.addWidget(self.saveButton)

        self.toggleThemeButton: TransparentToolButton = TransparentToolButton(FluentIcon.CONSTRACT, self)
        self.toggleThemeButton.setFixedSize(46, 32)
        self.titleBar.hBoxLayout.insertWidget(4, self.toggleThemeButton)

        setToolTipInfo(self.toggleThemeButton, "切换主题", 2500, ToolTipPosition.TOP)
        self.connectSignalSlot()

    def getSuffixName(self, file: str):
        return file.split(".")[-1]

    def _updateImage(self, path):
        if path:
            path = path[0]
            if self.getSuffixName(path) in self.imageTypes:
                self.image = path
                self.previewWidget.imageWidget.updateImage(path)
                self.fileWidget.setDefaultDir(os.path.dirname(path))
            else:
                InfoBar.error(
                    f"错误, 请选择图片类型文件: {self.imageTypes}",
                    "",
                    duration=3000,
                    position=InfoBarPosition.TOP,
                    parent=self
                )

    def _updateRadius(self):
        self.previewWidget.imageWidget.updateRadius(*self.optionView.getRadius())

    def _onAppliButtonClicked(self):
        self._updateRadius()
        InfoBar.success(
            f"设置圆角成功! 值(左上, 右上, 右下, 左下): {self.optionView.getRadius()}",
            "",
            duration=3000,
            position=InfoBarPosition.TOP,
            parent=self
        )

    def _onSaveButtonClicked(self):
        if not self.image:
            InfoBar.error(
                "图片保存失败,未选择图片文件!",
                "",
                duration=3000,
                isClosable=False,
                position=InfoBarPosition.TOP,
                parent=self
            )
            return
        filePath = os.path.dirname(self.image)
        if self.memorySavePathSwitchButton.isChecked():
            self.save(self.saveDir)
        else:
            saveDir = QFileDialog.getExistingDirectory(self, "选择保存文件夹", self.saveDir or filePath) + "/"
            self.save(saveDir)

    def save(self, saveDir: str):
        openButton: TransparentToolButton = TransparentToolButton(FluentIcon.FOLDER, self)
        setToolTipInfo(openButton, "打开保存目录", 2500, ToolTipPosition.TOP)
        suffix = self.saveTypes[self.saveTypeComboBox.currentIndex()]
        fileName = self.image.split(".")[0].split("/")[-1]
        if saveDir and saveDir != "/":
            if not self.memorySavePathSwitchButton.isEnabled():
                self.memorySavePathSwitchButton.setEnabled(True)
            self.saveDir = saveDir
            cfg.set(cfg.saveDir, saveDir)
            InfoBar.success(
                f"  保存成功! 文件路径: {saveDir}{fileName}_ClipResult.{suffix}  ",
                "",
                duration=-1,
                position=InfoBarPosition.TOP,
                parent=self
            ).addWidget(openButton)
            openButton.clicked.connect(lambda: subprocess.run(['explorer', os.path.normpath(saveDir)]))
            print(saveDir)
            print(
                customRoundPixmap(self.image, *self.optionView.getRadius()).toImage().save(
                    f"{saveDir}{fileName}_ClipResult.{suffix}", suffix
                )
            )

    def _onMemoryPathCheckedChanged(self, checked: bool):
        cfg.set(cfg.isMemorySavePath, checked)

    def connectSignalSlot(self):
        self.optionButton.clicked.connect(self.optionView.show)
        self.previewButton.clicked.connect(self.previewWidget.show)
        self.fileWidget.draggedChange.connect(self._updateImage)
        self.fileWidget.selectionChange.connect(self._updateImage)
        self.optionView.applyButton.clicked.connect(self._onAppliButtonClicked)
        self.toggleThemeButton.clicked.connect(toggleTheme)
        self.saveButton.clicked.connect(self._onSaveButtonClicked)
        self.memorySavePathSwitchButton.checkedChanged.connect(self._onMemoryPathCheckedChanged)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
