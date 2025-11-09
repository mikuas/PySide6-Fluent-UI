# coding:utf-8
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt

from PySide6FluentUI import PopupDrawerWidget, PopupDrawerPosition, TransparentToolButton, FluentIcon, FillPushButton, \
    FlyoutView, FlyoutDialog, FlyoutPosition
from examples.window.splitWidget.demo import Interface


class PopupDrawerInterface(Interface):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.viewLayout: QVBoxLayout = QVBoxLayout(self)
        self.settingButton: TransparentToolButton = TransparentToolButton(FluentIcon.SETTING, self)
        self.settingsDialog: FlyoutDialog = FlyoutDialog(self.settingButton, FlyoutPosition.BOTTOM, self)
        self.LeftPopupDrawer: PopupDrawerWidget = PopupDrawerWidget("LeftPopupDrawer", position=PopupDrawerPosition.LEFT, parent=self)
        self.topPopupDrawer: PopupDrawerWidget = PopupDrawerWidget("TopPopupDrawer", position=PopupDrawerPosition.TOP, parent=self)
        self.RightPopupDrawer: PopupDrawerWidget = PopupDrawerWidget("RightPopupDrawer", position=PopupDrawerPosition.RIGHT, parent=self)
        self.BottomPopupDrawer: PopupDrawerWidget = PopupDrawerWidget("BottomPopupDrawer", position=PopupDrawerPosition.BOTTOM, parent=self)

        self.lb: FillPushButton = FillPushButton("Left PopupDrawer", self)
        self.tb: FillPushButton = FillPushButton("Top PopupDrawer", self)
        self.rb: FillPushButton = FillPushButton("Right PopupDrawer", self)
        self.bb: FillPushButton = FillPushButton("Bottom PopupDrawer", self)

        self.settingButton.setFixedSize(self.titleBar.minBtn.size())
        self.titleBar.hBoxLayout.insertWidget(4, self.settingButton)

        self.viewLayout.setAlignment(Qt.AlignCenter)
        self.viewLayout.addWidget(self.lb)
        self.viewLayout.addWidget(self.tb)
        self.viewLayout.addWidget(self.rb)
        self.viewLayout.addWidget(self.bb)

        self.__initSettingsDialog()
        self.connectSignalSlot()

        self.topPopupDrawer.setEasingCurve()

    def __initSettingsDialog(self):
        self.settingsDialog
    
    def connectSignalSlot(self):
        super().connectSignalSlot()
        self.settingButton.clicked.connect(self.settingsDialog.show)
        self.lb.clicked.connect(self.LeftPopupDrawer.toggleDrawer)
        self.tb.clicked.connect(self.topPopupDrawer.toggleDrawer)
        self.rb.clicked.connect(self.RightPopupDrawer.toggleDrawer)
        self.bb.clicked.connect(self.BottomPopupDrawer.toggleDrawer)

def main():
    app = QApplication(sys.argv)
    window = PopupDrawerInterface()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
    
    ...

if __name__ == '__main__':
    main()