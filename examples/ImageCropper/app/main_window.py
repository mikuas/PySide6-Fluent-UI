# coding:utf-8
import sys
import subprocess
import os.path

from PySide6.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QFileDialog, QListWidgetItem
from PySide6.QtGui import QImageReader
from PySide6.QtCore import Qt

from PySide6FluentUI import SplitWidget, DragFileWidget, SubtitleLabel, PushButton, PrimaryPushButton, FluentIcon, \
    TransparentToolButton, setToolTipInfo, ToolTipPosition, toggleTheme, InfoBar, InfoBarPosition, SwitchButton

from .views.option_view import OptionView
from .views.preview_widget import PreviewWidget
from .utils.round_radius_utils import customRoundPixmap
from .utils.file_utils import getSuffixName
from .common.config import cfg


class MainWindow(SplitWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 520)
        self.viewLayout: QVBoxLayout = QVBoxLayout(self)
        self.viewLayout.setContentsMargins(11, 38, 11, 11)
        self.imagePath: str = ""
        self.saveDir: str = cfg.saveDir.value
        self.imageTypes: list[str] = [f.data().decode() for f in QImageReader.supportedImageFormats()]

        print(f"{self.imageTypes = }")
        self.fileFilter: str = "图像文件 ("
        for f in self.imageTypes:
            self.fileFilter += f"*.{f} "
        self.fileFilter += ");; 所有文件(*.*)"

        self.titleLabel: SubtitleLabel = SubtitleLabel("圆角图片裁剪工具", self)
        self.memorySavePathSwitchButton: SwitchButton = SwitchButton(self)
        self.memorySavePathSwitchButton.setChecked(cfg.isMemorySavePath.value)
        self.fileWidget: DragFileWidget = DragFileWidget(
            fileFilter=self.fileFilter,
            isDashLine=True,
            parent=self
        )
        self.fileWidget.setLabelText("拖动图像文件到此")

        self.optionButton: PushButton = PushButton("设置", self)
        self.previewButton: PushButton = PushButton("预览", self)
        self.saveButton: PrimaryPushButton = PrimaryPushButton("保存", self)
        self.optionView: OptionView = OptionView(self)
        self.previewWidget: PreviewWidget = PreviewWidget(self.previewButton, self)

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
        buttonLayout.addWidget(self.saveButton)

        self.toggleThemeButton: TransparentToolButton = TransparentToolButton(FluentIcon.CONSTRACT, self)
        self.toggleThemeButton.setFixedSize(46, 32)
        self.titleBar.hBoxLayout.insertWidget(4, self.toggleThemeButton)

        setToolTipInfo(self.toggleThemeButton, "切换主题", 2500, ToolTipPosition.TOP)
        self.connectSignalSlot()

    def _updateSelectedImage(self, item: QListWidgetItem):
        if item:
            path = item.data(Qt.ItemDataRole.UserRole)
            self.imagePath = path
            self.previewWidget.imageWidget.updateImage(path)

    def _updateImage(self, paths):
        if paths:
            files = []
            self.optionView.roundListWidget.clear()
            for path in paths:
                if getSuffixName(path) in self.imageTypes:
                    files.append(path)
                    item = QListWidgetItem(path.split("/")[-1])
                    item.setData(Qt.ItemDataRole.UserRole, path)
                    self.optionView.roundListWidget.addItem(item)
            path = files[0]
            fileDir = os.path.dirname(path)
            self.imagePath = path
            self.optionView.roundListWidget.setCurrentRow(0)
            self.optionView.imageListLabel.setText(f"图片列表 目录: {fileDir}")
            self.optionView.imageCountLabel.setText(f"图片数量: {len(files)}")
            self.previewWidget.imageWidget.updateImage(path)
            self.fileWidget.setDefaultDir(fileDir)

    def _updateRadius(self):
        self.previewWidget.imageWidget.updateRadius(*self.optionView.radiusView.getRadius())

    def _onAppliButtonClicked(self):
        self._updateRadius()
        InfoBar.success(
            f"设置圆角成功! 值(左上, 右上, 右下, 左下): {self.optionView.radiusView.getRadius()}",
            "",
            duration=3000,
            position=InfoBarPosition.TOP,
            parent=self
        )

    def _onSaveButtonClicked(self):
        if not self.imagePath:
            InfoBar.error(
                "图片保存失败,未选择图片文件!",
                "",
                duration=3000,
                isClosable=False,
                position=InfoBarPosition.TOP,
                parent=self
            )
            return
        if self.memorySavePathSwitchButton.isChecked():
            self.save(self.saveDir)
        else:
            saveDir = QFileDialog.getExistingDirectory(self, "选择保存文件夹", self.saveDir or os.path.dirname(self.imagePath)) + "/"
            self.save(saveDir)

    def save(self, saveDir: str):
        suffix = self.optionView.saveTypes[self.optionView.saveTypeComboBox.currentIndex()]
        tmp = self.imagePath.split("/")[-1].split(".")

        print(f"Split = {tmp}")

        if len(tmp) > 2:
            fileName = ""
            for _ in tmp[:-1]:
                fileName = fileName + _ + "_"
        else:
            fileName = tmp[0]
        print(f"{fileName = }")

        if saveDir and saveDir != "/":
            if not self.memorySavePathSwitchButton.isEnabled():
                self.memorySavePathSwitchButton.setEnabled(True)
            self.saveDir = saveDir
            cfg.set(cfg.saveDir, saveDir)
            print(f"{saveDir = }")
            src = os.path.join(saveDir, fileName)
            result = customRoundPixmap(self.imagePath, *self.optionView.radiusView.getRadius()).toImage().save(f"{src}_ClipResult.{suffix}", suffix)

            if result:
                openButton: TransparentToolButton = TransparentToolButton(FluentIcon.FOLDER)
                setToolTipInfo(openButton, "打开保存目录", 2500, ToolTipPosition.TOP)
                openButton.clicked.connect(lambda: subprocess.run(['explorer', os.path.normpath(saveDir)]))

                InfoBar.success(
                    f"  保存成功! 文件路径: {src}_ClipResult.{suffix}  ",
                    "",
                    duration=-1,
                    position=InfoBarPosition.TOP,
                    parent=self
                ).addWidget(openButton)
                if self.optionView.roundListWidget.count() > 0:
                    print(f"Count: {self.optionView.roundListWidget.count()}")
                    print(f"Current Row: {self.optionView.roundListWidget.currentRow()}")
                    self.optionView.roundListWidget.takeItem(self.optionView.roundListWidget.currentRow())
                    print(f"TakeItemCount: {self.optionView.roundListWidget.count()}\n")
                    nextItem = self.optionView.roundListWidget.item(0)
                    self.optionView.roundListWidget.setCurrentRow(0)
                    if nextItem:
                        self.imagePath = nextItem.data(Qt.ItemDataRole.UserRole)
                        self.previewWidget.imageWidget.updateImage(self.imagePath)
                    else:
                        self.imagePath = ""
                        self.previewWidget.imageWidget.updateImage("")
            else:
                InfoBar.error(
                    "文件保存失败",
                    "",
                    duration=3500,
                    position=InfoBarPosition.TOP,
                    parent=self
                )

    def resizeEvent(self, e):
        self.optionView.setFixedWidth(self.width() // 2)
        self.optionView._adjustDrawer()
        super().resizeEvent(e)

    def _onMemoryPathCheckedChanged(self, checked: bool):
        cfg.set(cfg.isMemorySavePath, checked)

    def _moveSelection(self, offset: int):
        currentRow = self.optionView.roundListWidget.currentRow()
        newRow = currentRow + offset
        count = self.optionView.roundListWidget.count()

        if 0 <= currentRow < count:
            self.optionView.roundListWidget.setCurrentRow(newRow)
            return False
        return True

    def _onPreviousButtonClicked(self):
        self._moveSelection(-1)

    def _onNextButtonClicked(self):
        self._moveSelection(1)

    def connectSignalSlot(self):
        self.optionButton.clicked.connect(self.optionView.toggleDrawer)
        self.previewButton.clicked.connect(self.previewWidget.show)
        self.fileWidget.draggedChange.connect(self._updateImage)
        self.fileWidget.selectionChange.connect(self._updateImage)

        self.optionView.radiusView.applyButton.clicked.connect(self._onAppliButtonClicked)
        self.optionView.roundListWidget.currentItemChanged.connect(self._updateSelectedImage)

        self.previewWidget.imageWidget.previousButton.clicked.connect(self._onPreviousButtonClicked)
        self.previewWidget.imageWidget.nextButton.clicked.connect(self._onNextButtonClicked)

        self.toggleThemeButton.clicked.connect(toggleTheme)
        self.saveButton.clicked.connect(self._onSaveButtonClicked)
        self.memorySavePathSwitchButton.checkedChanged.connect(self._onMemoryPathCheckedChanged)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
