# coding:utf-8
import re
import sys

from PySide6.QtCore import QRectF, QTimer
from PySide6.QtGui import QPainter, QColor, Qt
from PySide6.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout

from PySide6FluentUI import PushButton, FluentIcon, SplitWidget, toggleTheme, isDarkTheme, setCustomStyleSheet, \
    drawRoundRect, qconfig, RoundPushButton, RoundToolButton, OutlinePushButton, OutlineToolButton, FillPushButton, \
    FillToolButton, FlyoutDialog, TransparentToolButton, setToolTipInfo, CaptionLabel, ColorPickerButton, themeColor, \
    FlyoutPosition, DropDownColorPalette, ComboBox, BodyLabel
from examples.window.splitWidget.demo import Interface


class MainWindow(Interface):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setMicaEffectEnabled(True)
        self.viewLayout: QVBoxLayout = QVBoxLayout(self)
        self.viewLayout.setContentsMargins(24, 24, 24, 24)

        self.pushButton: PushButton = PushButton(FluentIcon.HOME, "PushButton", self)
        self.roundPushButton: RoundPushButton = RoundPushButton(FluentIcon.HOME, "roundPushButton", self)
        self.roundToolButton: RoundToolButton = RoundToolButton(FluentIcon.HOME, self)

        self.outlinePushButton: OutlinePushButton = OutlinePushButton(FluentIcon.HOME, "OutlinePushButton", self)
        self.outlineToolButton: OutlineToolButton = OutlineToolButton(FluentIcon.GITHUB, self)

        self.fillPushButton: FillPushButton = FillPushButton(FluentIcon.ACCEPT, "FillPushButton", self)
        self.fillToolButton: FillToolButton = FillToolButton(FluentIcon.ACCEPT, self)

        self.viewLayout.addWidget(self.pushButton)
        self.viewLayout.addWidget(self.roundPushButton)
        self.viewLayout.addWidget(self.roundToolButton, 0, Qt.AlignHCenter)
        self.viewLayout.addWidget(self.outlinePushButton)
        self.viewLayout.addWidget(self.outlineToolButton, 0, Qt.AlignHCenter)
        self.viewLayout.addWidget(self.fillPushButton)
        self.viewLayout.addWidget(self.fillToolButton, 0, Qt.AlignRight)

        print(min(self.roundPushButton.width(), self.roundPushButton.height()) / 2)
        self.roundPushButton.setRadius(0, 15, 0, 15)
        self.roundToolButton.setRadius(15, 0, 15, 0)

        self.outlinePushButton.setRadius(8, 8, 8, 8)
        self.outlinePushButton.setOutlineColor("deeppink")
        self.fillPushButton.setFillColor("deepskyblue")
        self.fillToolButton.setFillColor("gray")
        self.fillToolButton.setMinimumWidth(256)

        self.outlinePushButton.setRadius(15, 15, 0, 0)
        r: int = int(min(self.fillPushButton.width(), self.fillPushButton.height()) / 2)
        self.fillPushButton.setRadius(r, r, r, r)

        self.fillToolButton.setRadius(15, 0, 0, 15)

        self.settingButton: TransparentToolButton = TransparentToolButton(FluentIcon.SETTING, self)
        self.settingButton.setFixedSize(46, 32)
        self.titleBar.hBoxLayout.insertWidget(4, self.settingButton)

        setToolTipInfo(self.settingButton, "设置", 2500)

        self.__initSettingsWidget()
        self.connectSignalSlot()

    def __initSettingsWidget(self):
        self.settingDialog: FlyoutDialog = FlyoutDialog(self.settingButton, FlyoutPosition.LEFT, self)
        self.settingDialog.setParent(self.window())
        self.settingDialog.viewLayout.setContentsMargins(24, 24, 24, 24)
        self.settingDialog.viewLayout.setSpacing(16)

        self.colorLayout: QHBoxLayout = QHBoxLayout()
        self.selectedColorTitle: BodyLabel = BodyLabel("选择OutlineButton边框颜色和FillButton填充颜色", self)
        self.colorPalette: DropDownColorPalette = DropDownColorPalette(self)
        self.colorLayout.setSpacing(24)
        self.colorLayout.addWidget(self.selectedColorTitle)
        self.colorLayout.addWidget(self.colorPalette)
        self.settingDialog.viewLayout.addLayout(self.colorLayout)

        rs = [str(r) for r in range(16)]
        self.radiusTitle: BodyLabel = BodyLabel("设置圆角弧度(左上, 右上, 右下, 左下)", self)
        self.settingDialog.viewLayout.addWidget(self.radiusTitle, 0, Qt.AlignCenter)
        self.radiusLayout: QHBoxLayout = QHBoxLayout()
        self.tlComboBox: ComboBox = ComboBox(self)
        self.trComboBox: ComboBox = ComboBox(self)
        self.brComboBox: ComboBox = ComboBox(self)
        self.blComboBox: ComboBox = ComboBox(self)

        for c in [self.tlComboBox, self.trComboBox, self.brComboBox, self.blComboBox]:
            c.addItems(rs)
            c.setCurrentText("8")
            self.radiusLayout.addWidget(c)
        self.settingDialog.viewLayout.addLayout(self.radiusLayout)

        self.applyRadiusButton: FillPushButton = FillPushButton("应用圆角弧度", self)
        self.settingDialog.viewLayout.addWidget(self.applyRadiusButton, 1)

    def _updateButtonColor(self, color: QColor):
        self.outlinePushButton.setOutlineColor(color)
        self.outlineToolButton.setOutlineColor(color)
        self.fillPushButton.setFillColor(color)
        self.fillToolButton.setFillColor(color)

    def _updateRadius(self):
        tl, tr, br, bl = self.tlComboBox.currentIndex(), self.trComboBox.currentIndex(), self.brComboBox.currentIndex(), self.blComboBox.currentIndex()
        self.roundPushButton.setRadius(tl, tr, br, bl)
        self.roundToolButton.setRadius(tl, tr, br, bl)
        self.outlinePushButton.setRadius(tl, tr, br, bl)
        self.outlineToolButton.setRadius(tl, tr, br, bl)

    def connectSignalSlot(self):
        super().connectSignalSlot()
        self.settingButton.clicked.connect(self.settingDialog.show)
        self.colorPalette.colorChanged.connect(self._updateButtonColor)
        self.applyRadiusButton.clicked.connect(self._updateRadius)

        self.colorPalette.customColorButton.clicked.connect(self.settingDialog.hide)

    def update(self):
        super().update()
        try:
            self.fillToolButton.move(self.width() - self.fillToolButton.width(), self.fillToolButton.y())
        except AttributeError: ...

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.fillToolButton.move(self.width() - self.fillToolButton.width(), self.fillToolButton.y())


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.resize(800, 520)
    sys.exit(app.exec())
    ...


if __name__ == '__main__':
    main()