# coding:utf-8
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy

from PySide6FluentUI import TransparentToolButton, FluentIcon, FillPushButton, FlyoutDialog, FlyoutPosition, \
    DropDownColorPalette, FillToolButton, AnimatedMenu, Action, ColorDialog, themeColor, ColorView, FocusLineEdit
from examples.window.splitWidget.demo import Interface


class FillButtonInterface(Interface):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.settingsMenu: AnimatedMenu = AnimatedMenu("title", self)
        self.viewLayout: QVBoxLayout = QVBoxLayout(self)
        self.settingsDialog: FlyoutDialog = FlyoutDialog(self, parent=self)
        self.colorDialog: ColorDialog = ColorDialog(themeColor(), "选择填充颜色", self, True)
        self.colorDialog.setWindowFlags(self.colorDialog.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)

        pbLayout: QHBoxLayout = QHBoxLayout()
        self.pb1: FillPushButton = FillPushButton(FluentIcon.HOME, "主页", self)
        self.pb2: FillPushButton = FillPushButton(FluentIcon.GITHUB, "GitHub", self)
        self.pb3: FillPushButton = FillPushButton("设置", self)
        self.pb4: FillPushButton = FillPushButton("关于", self)

        self.pb2.setEnabled(False)
        self.pb3.setRadius(15, 15, 15, 15)
        self.pb4.setEnabled(False)
        self.pb4.setRadius(15, 15, 15, 15)
        self.pb1.setFillColor("#787979")
        self.pb3.setFillColor("#9d5d00")
        pbLayout.addWidget(self.pb1)
        pbLayout.addWidget(self.pb2)
        pbLayout.addWidget(self.pb3)
        pbLayout.addWidget(self.pb4)

        tbLayout: QHBoxLayout = QHBoxLayout()
        self.tb1: FillToolButton = FillToolButton(FluentIcon.HOME, self)
        self.tb2: FillToolButton = FillToolButton(FluentIcon.GITHUB, self)
        self.tb3: FillToolButton = FillToolButton(FluentIcon.SETTING, self)
        self.tb4: FillToolButton = FillToolButton(FluentIcon.AIRPLANE, self)

        self.tb2.setEnabled(False)
        self.tb3.setRadius(15, 15, 15, 15)
        self.tb4.setEnabled(False)
        self.tb4.setRadius(15, 15, 15, 15)
        self.tb1.setFillColor("#f6ffed")
        self.tb1.setTextColor("#8fda69", "#8fda69")
        self.tb3.setFillColor("#d83f40")
        self.tb1.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.tb2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.tb3.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.tb4.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        tbLayout.addWidget(self.tb1)
        tbLayout.addWidget(self.tb2)
        tbLayout.addWidget(self.tb3)
        tbLayout.addWidget(self.tb4)

        self.viewLayout.addLayout(pbLayout)
        self.viewLayout.addLayout(tbLayout)

        self.colorDialog.hide()
        print(self.pb1.styleSheet())

        self.bgcAction: Action = Action("设置按钮颜色", self, triggered=self._onBackgroundColorChange)
        self.textCAction: Action = Action("设置文本或图标颜色", self, triggered=self._onTextColorChange)
        self.radiusAction: Action = Action("设置Radius", self, triggered=self._onRadiusChange)

        self.__initSettingsDialog()
        self.connectSignalSlot()

    def __initSettingsDialog(self):
        self.radiusEdit: FocusLineEdit = FocusLineEdit(self)
        self.radiusEdit.setValidator(QIntValidator(self))
        self.radiusEdit.setPlaceholderText("请输入圆角值, 回车确定")

        self.settingsDialog.viewLayout.addWidget(self.radiusEdit)

    def connectSignalSlot(self):
        super().connectSignalSlot()
        self.radiusEdit.returnPressed.connect(self._onRadiusEditReturnPressed)

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
            self.settingsMenu.addActions([self.bgcAction, self.textCAction, self.radiusAction])
            self.settingsMenu.exec(event.globalPos())

    def _onBackgroundColorChange(self):
        if self.showColorDialog():
            self.property("currentWidget").setFillColor(self.colorDialog.color)

    def _onTextColorChange(self):
        if self.showColorDialog():
            self.property("currentWidget").setTextColor(self.colorDialog.color, self.colorDialog.color)

    def _onRadiusChange(self):
        w = self.property("currentWidget")
        if w:
            self.settingsDialog.setTarget(w)
            self.settingsDialog.show()

    def showColorDialog(self):
        self.settingsMenu.hide()
        self.colorDialog.raise_()
        return self.colorDialog.exec() and self.property("currentWidget")


def main():
    app = QApplication(sys.argv)
    window = FillButtonInterface()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
    ...

if __name__ == '__main__':
    main()