# coding:utf-8
import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon, Qt

from PySide6FluentUI import FluentWindow, FluentIcon, NavigationItemPosition, FluentTranslator, TransparentToolButton, \
    toggleTheme

from .views.home_interface import HomeInterface
from .views.icon_interface import IconInterface
from .views.basic_input_interface import BasicInputInterface
from .views.dialog_interface import DialogInterface
from .views.layout_interface import LayoutInterface
from .views.navigation_interface import NavigationInterface
from .views.status_interface import StatusInterface
from .views.view_interface import ViewInterface
from .views.setting_interface import SettingInterface


class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("gallery")
        self.setWindowIcon(QIcon(":/gallery/icons/app.ico"))

        self.translator: FluentTranslator = FluentTranslator()
        QApplication.installTranslator(self.translator)

        self.toggleThemeButton: TransparentToolButton = TransparentToolButton(FluentIcon.CONSTRACT, self)
        self.toggleThemeButton.clicked.connect(lambda: toggleTheme(True))
        self.toggleThemeButton.setFixedSize(self.titleBar.maxBtn.size())
        self.titleBar.hBoxLayout.insertWidget(3, self.toggleThemeButton, 0, Qt.AlignRight | Qt.AlignTop)
        
        self.homeInterface: HomeInterface = HomeInterface(self)
        self.iconInterface: IconInterface = IconInterface(self)
        self.basicInputInterface: BasicInputInterface = BasicInputInterface(self)
        self.dialogInterface: DialogInterface = DialogInterface(self)
        self.layoutInterface: LayoutInterface = LayoutInterface(self)
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
            self.layoutInterface,
            FluentIcon.LAYOUT,
            "布局",
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

    def show(self):
        screen = QApplication.primaryScreen()
        pr = screen.devicePixelRatio()
        size = screen.size()
        w, h = size.width(), size.height()
        self.resize(w * pr // 2.5, h * pr // 2.5)

        self.move((w - self.width()) // 2, (h - self.height()) // 2)
        super().show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    app.setStyleSheet(window.styleSheet())
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())