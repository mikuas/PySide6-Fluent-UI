# coding:utf-8
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy

from PySide6FluentUI import FluentIcon, OutlinePushButton, OutlineToolButton, FlyoutDialog, AnimatedMenu, ColorDialog, \
    themeColor, Action, FocusLineEdit
from examples.window.splitWidget.demo import Interface


class OutlineButtonInterface(Interface):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.settingsMenu: AnimatedMenu = AnimatedMenu("title", self)
        self.viewLayout: QVBoxLayout = QVBoxLayout(self)
        self.settingsDialog: FlyoutDialog = FlyoutDialog(self, parent=self)
        self.colorDialog: ColorDialog = ColorDialog(themeColor(), "选择填充颜色", self, True)
        self.colorDialog.setWindowFlags(self.colorDialog.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)

        pbLayout: QHBoxLayout = QHBoxLayout()
        self.pb1: OutlinePushButton = OutlinePushButton(FluentIcon.HOME, "主页", self)
        self.pb2: OutlinePushButton = OutlinePushButton(FluentIcon.GITHUB, "GitHub", self)
        self.pb3: OutlinePushButton = OutlinePushButton("设置", self)
        self.pb4: OutlinePushButton = OutlinePushButton("关于", self)

        self.pb2.setEnabled(False)
        self.pb3.setRadius(8, 8, 8, 8)
        self.pb4.setEnabled(False)
        self.pb4.setRadius(8, 8, 8, 8)
        pbLayout.addWidget(self.pb1)
        pbLayout.addWidget(self.pb2)
        pbLayout.addWidget(self.pb3)
        pbLayout.addWidget(self.pb4)

        tbLayout: QHBoxLayout = QHBoxLayout()
        self.tb1: OutlineToolButton = OutlineToolButton(FluentIcon.HOME, self)
        self.tb2: OutlineToolButton = OutlineToolButton(FluentIcon.GITHUB, self)
        self.tb3: OutlineToolButton = OutlineToolButton(FluentIcon.SETTING, self)
        self.tb4: OutlineToolButton = OutlineToolButton(FluentIcon.LABEL, self)

        self.tb2.setEnabled(False)
        self.tb3.setRadius(8, 8, 8, 8)
        self.tb4.setEnabled(False)
        self.tb4.setRadius(8, 8, 8, 8)
        tbLayout.addWidget(self.tb1)
        tbLayout.addWidget(self.tb2)
        tbLayout.addWidget(self.tb3)
        tbLayout.addWidget(self.tb4)
        self.tb1.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.tb2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.tb3.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.tb4.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.viewLayout.addLayout(pbLayout)
        self.viewLayout.addLayout(tbLayout)

        self.otcAction: Action = Action("设置OutlineColor", self, triggered=self._onOutlineColorChange)
        self.widthAction: Action = Action("设置OutlineWidth", self, triggered=self._onOutlineWidthChange)
        self.radiusAction: Action = Action("设置Radius", self, triggered=self._onRadiusChange)

        self.colorDialog.hide()
        self.__initSettingsDialog()
        self.connectSignalSlot()

    def __initSettingsDialog(self):
        self.radiusEdit: FocusLineEdit = FocusLineEdit(self)
        self.radiusEdit.setValidator(QIntValidator(self))
        self.radiusEdit.setPlaceholderText("请输入圆角值, 回车确定")

        self.widthEdit: FocusLineEdit = FocusLineEdit(self)
        self.widthEdit.setPlaceholderText("请输入线宽, 回车确定")
        self.radiusEdit.setValidator(QIntValidator(self))

        self.settingsDialog.viewLayout.addWidget(self.radiusEdit)
        self.settingsDialog.viewLayout.addWidget(self.widthEdit)

    def connectSignalSlot(self):
        super().connectSignalSlot()
        self.radiusEdit.returnPressed.connect(self._onRadiusEditReturnPressed)
        self.widthEdit.returnPressed.connect(self._onOutlineWidthEditReturnPressed)

    def _onRadiusEditReturnPressed(self):
        self.settingsDialog.hide()
        w = self.property("currentWidget")
        if w:
            radius = int(self.radiusEdit.text())
            w.setRadius(radius, radius, radius, radius)

    def contextMenuEvent(self, event):
        super().contextMenuEvent(event)
        w = self.childAt(event.pos())
        self.setProperty("currentWidget", w)
        self.settingsMenu.clear()
        if w:
            self.settingsMenu.addActions([self.otcAction, self.radiusAction])
            self.settingsMenu.exec(event.globalPos())

    def _onOutlineColorChange(self):
        if self.showColorDialog():
            self.property("currentWidget").setOutlineColor(self.colorDialog.color)

    def _onOutlineWidthEditReturnPressed(self):
        self.settingsDialog.hide()
        w = self.property("currentWidget")
        if w:
            width = float(self.widthEdit.text())
            w.setOutlineWidth(width)

    def _onRadiusChange(self):
        w = self.property("currentWidget")
        if w:
            self.radiusEdit.setVisible(True)
            self.widthEdit.setVisible(False)
            self.settingsDialog.setTarget(w)
            self.settingsDialog.show()

    def _onOutlineWidthChange(self):
        w = self.property("currentWidget")
        if w:
            self.radiusEdit.setVisible(False)
            self.widthEdit.setVisible(True)
            self.settingsDialog.setTarget(w)
            self.settingsDialog.show()

    def showColorDialog(self):
        self.settingsMenu.hide()
        self.colorDialog.raise_()
        return self.colorDialog.exec() and self.property("currentWidget")


def main():
    app = QApplication(sys.argv)
    window = OutlineButtonInterface()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
    ...

if __name__ == '__main__':
    main()