# coding:utf-8
import sys

from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy

from PySide6FluentUI import FluentIcon, RoundPushButton, RoundToolButton, FlyoutDialog, FocusLineEdit, AnimatedMenu, \
    Action
from examples.window.splitWidget.demo import Interface


class RoundButtonInterface(Interface):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.settingsMenu: AnimatedMenu = AnimatedMenu(parent=self)

        self.settingsDialog: FlyoutDialog = FlyoutDialog(self, parent=self)
        self.radiusEdit: FocusLineEdit = FocusLineEdit(self)
        self.radiusEdit.setPlaceholderText("输入Radius, 回车确定")
        self.radiusEdit.setValidator(QIntValidator(self))
        self.settingsDialog.viewLayout.addWidget(self.radiusEdit)

        self.viewLayout: QVBoxLayout = QVBoxLayout(self)

        pbLayout: QHBoxLayout = QHBoxLayout()
        self.pb1: RoundPushButton = RoundPushButton(FluentIcon.HOME, "主页", self)
        self.pb2: RoundPushButton = RoundPushButton(FluentIcon.GITHUB, "GitHub", self)
        self.pb3: RoundPushButton = RoundPushButton("设置", self)
        self.pb4: RoundPushButton = RoundPushButton("关于", self)

        self.pb2.setEnabled(False)
        self.pb3.setRadius(8, 8, 8, 8)
        self.pb4.setEnabled(False)
        self.pb4.setRadius(8, 8, 8, 8)
        pbLayout.addWidget(self.pb1)
        pbLayout.addWidget(self.pb2)
        pbLayout.addWidget(self.pb3)
        pbLayout.addWidget(self.pb4)

        tbLayout: QHBoxLayout = QHBoxLayout()
        self.tb1: RoundToolButton = RoundToolButton(FluentIcon.HOME, self)
        self.tb2: RoundToolButton = RoundToolButton(FluentIcon.GITHUB, self)
        self.tb3: RoundToolButton = RoundToolButton(FluentIcon.VIDEO, self)
        self.tb4: RoundToolButton = RoundToolButton(FluentIcon.SETTING, self)

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
        
        self.radiusAction: Action = Action("设置圆角弧度", self, triggered=self._onRadiusChange)
        
        self.connectSignalSlot()

    def _onRadiusEditReturnPressed(self):
        self.settingsDialog.hide()
        w = self.property("currentWidget")
        if w:
            radius = int(self.radiusEdit.text())
            w.setRadius(radius, radius, radius, radius)

    def _onRadiusChange(self):
        w = self.property("currentWidget")
        if w:
            self.settingsDialog.setTarget(w)
            self.settingsDialog.show()

    def connectSignalSlot(self):
        super().connectSignalSlot()
        self.radiusEdit.returnPressed.connect(self._onRadiusEditReturnPressed)

    def contextMenuEvent(self, event):
        w = self.childAt(event.pos())
        self.setProperty("currentWidget", w)
        self.settingsMenu.clear()
        if w:
            self.settingsMenu.addAction(self.radiusAction)
            self.settingsMenu.exec(event.globalPos())


def main():
    app = QApplication(sys.argv)
    window = RoundButtonInterface()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
    ...

if __name__ == '__main__':
    main()