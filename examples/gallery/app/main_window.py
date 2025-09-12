# coding:utf-8
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from PySide6FluentUI import FluentWindow, FluentIcon, NavigationItemPosition, FluentTranslator

from .views.home_interface import HomeInterface
from .views.icon_interface import IconInterface
from .views.basic_input_interface import BasicInputInterface
from .views.dialog_interface import DialogInterface
from .views.navigation_interface import NavigationInterface
from .views.status_interface import StatusInterface
from .views.view_interface import ViewInterface
from .views.setting_interface import SettingInterface


class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("gallery")
        # self.setWindowIcon(QIcon(str(Path(__file__).resolve().parents[1] / "resources" / "icons" / "app.ico")))
        self.setWindowIcon(QIcon(":/gallery/icons/app.ico"))

        self.translator: FluentTranslator = FluentTranslator()
        QApplication.installTranslator(self.translator)
        
        self.homeInterface: HomeInterface = HomeInterface(self)
        self.iconInterface: IconInterface = IconInterface(self)
        self.basicInputInterface: BasicInputInterface = BasicInputInterface(self)
        self.dialogInterface: DialogInterface = DialogInterface(self)
        self.navigationInterface_: NavigationInterface = NavigationInterface(self)
        self.statusInterface: StatusInterface = StatusInterface(self)
        self.viewInterface: ViewInterface = ViewInterface(self)
        self.settingInterface: SettingInterface = SettingInterface(self)
        
        self.initNavigation()
    
    def initNavigation(self):
        self.addSubInterface(
            self.homeInterface,
            FluentIcon.HOME,
            "主页",
            NavigationItemPosition.SCROLL
        )
        self.addSubInterface(
            self.iconInterface,
            FluentIcon.EMOJI_TAB_SYMBOLS,
            "图标",
            NavigationItemPosition.SCROLL
        )
        self.navigationInterface.addSeparator(NavigationItemPosition.SCROLL)
        self.addSubInterface(
            self.basicInputInterface,
            FluentIcon.CHECKBOX,
            "基本输入",
            NavigationItemPosition.SCROLL
        )
        self.addSubInterface(
            self.dialogInterface,
            FluentIcon.MESSAGE,
            "对话框和弹出窗口",
            NavigationItemPosition.SCROLL
        )
        self.addSubInterface(
            self.navigationInterface_,
            FluentIcon.MENU,
            "导航",
            NavigationItemPosition.SCROLL
        )
        self.addSubInterface(
            self.statusInterface,
            FluentIcon.CHAT,
            "状态和信息",
            NavigationItemPosition.SCROLL
        )
        self.addSubInterface(
            self.viewInterface,
            FluentIcon.VIEW,
            "视图",
            NavigationItemPosition.SCROLL
        )
        
        self.addSubInterface(
            self.settingInterface,
            FluentIcon.SETTING,
            "设置",
            NavigationItemPosition.BOTTOM
        )

    def showEvent(self, event):
        super().showEvent(event)
        screen = QApplication.primaryScreen()
        pr = screen.devicePixelRatio()
        size = screen.size()
        w, h = size.width(), size.height()
        self.resize(w * pr // 2.5, h * pr // 2.5)

        self.move((w - self.width()) // 2, (h - self.height()) // 2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())