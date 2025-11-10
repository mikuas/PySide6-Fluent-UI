# coding:utf-8
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget, QVBoxLayout, QApplication

from PySide6FluentUI import FluentIcon, SlidingNavigationBar, SlidingToolNavigationBar, InfoBadge, SubtitleLabel, \
    MenuBar, Action

from ..widgets.basic_interface import Interface


class NavigationInterface(Interface):
    def __init__(self, parent=None):
        super().__init__("导航", "PySide6FluentUI.components.widgets", parent)
        self.setObjectName("NavigationInterface")
        self.vBoxLayout.addWidget(self.scrollArea)

        """ menu bar """
        self.menuBar: MenuBar = MenuBar(self)

        """ file menu """
        self.fileMenu = self.menuBar.createMenu("文件(&F)")
        self.fileMenu.addActions([
            QAction("新建标签页", self, shortcut="Ctrl+N", triggered=lambda: print("新建标签页")),
            QAction("新建窗口", self, shortcut="Ctrl+Shift+N", triggered=lambda: print("新建窗口")),
            QAction("新建Markdown选项卡", self, triggered=lambda: print("新建Markdown选项卡")),
            QAction("打开", self, shortcut="Ctrl+O", triggered=lambda: print("打开")),
        ])

        self.fileSubMenu = self.menuBar.createMenu("最近使用")
        self.fileSubMenu.addAction(QAction("没有最近使用的文件", self))
        self.fileMenu.addMenu(self.fileSubMenu)

        self.fileMenu.addActions([
            QAction("保存", self, shortcut="Ctrl+S", triggered=lambda: print("保存")),
            QAction("另存为", self, shortcut="Ctrl+Shift+S", triggered=lambda: print("另存为")),
            QAction("全部保存", self, shortcut="Ctrl+Alt+S", triggered=lambda: print("全部保存")),
        ])
        self.fileMenu.addSeparator()

        self.fileMenu.addActions([
            QAction("页面设置", self, triggered=lambda: print("页面设置")),
            QAction("打印", self, shortcut="Ctrl+P", triggered=lambda: print("打印"))
        ])
        self.fileMenu.addSeparator()

        self.fileMenu.addActions([
            QAction("关闭选项卡", self, shortcut="Ctrl+W", triggered=lambda: print("关闭选项卡")),
            QAction("关闭窗口", self, shortcut="Ctrl+Shift+W", triggered=lambda: print("关闭窗口")),
            QAction("退出", self, shortcut="Ctrl+Q")
        ])

        """ edit menu """
        self.editMenu = self.menuBar.createMenu("编辑(&E)")
        self.editMenu.addAction(QAction("撤销", self, shortcut="Ctrl+Z", triggered=lambda: print("撤销")))
        self.editMenu.addSeparator()

        self.editMenu.addActions([
            Action(FluentIcon.CUT, "剪切", self, shortcut="Ctrl+X", triggered=lambda: print("剪切")),
            Action(FluentIcon.COPY, "复制", self, shortcut="Ctrl+C", triggered=lambda: print("复制")),
            Action(FluentIcon.PASTE, "粘贴", self, shortcut="Ctrl+V", triggered=lambda: print("粘贴")),
            Action(FluentIcon.DELETE, "删除", self, shortcut="Del", triggered=lambda: print("删除"))
        ])
        self.editMenu.addSeparator()

        self.editMenu.addActions([
            QAction("清除格式设置", self, triggered=lambda: print("清除格式设置")),
            QAction("使用必应搜索", self, triggered=lambda: print("使用必应搜索"))
        ])
        self.editMenu.addSeparator()

        self.editMenu.addActions([
            QAction("查找", self, shortcut="Ctrl+F", triggered=lambda: print("查找")),
            QAction("查找上一个", self, shortcut="F3", triggered=lambda: print("查找上一个")),
            QAction("查找下一个", self, shortcut="Shift+F3", triggered=lambda: print("查找下一个")),
            QAction("替换", self, shortcut="Ctrl+H", triggered=lambda: print("替换")),
            QAction("转到", self, shortcut="Ctrl+G", triggered=lambda: print("转到")),
        ])
        self.editMenu.addSeparator()

        self.editMenu.addActions([
            QAction("全选", self, shortcut="Ctrl+A", triggered=lambda: print("全选")),
            QAction("时间/日期", self, shortcut="F5", triggered=lambda: print("时间/日期")),
        ])
        self.editMenu.addSeparator()

        self.editMenu.addAction(QAction("字体", self, triggered=lambda: print("字体")))

        """ view menu """
        self.viewMenu = self.menuBar.createMenu("查看(&V)")
        self.zoomSubMenu = self.menuBar.createMenu("缩放")
        self.zoomSubMenu.addActions([
            QAction("放大", self, shortcut="Ctrl++", triggered=lambda: print("放大")),
            QAction("缩小", self, shortcut="Ctrl+-", triggered=lambda: print("缩小")),
            QAction("还原默认缩放", self, shortcut="Ctrl+R", triggered=lambda: print("还原默认缩放"))
        ])
        self.viewMenu.addMenu(self.zoomSubMenu)
        self.viewMenu.addActions([
            QAction("状态栏", self, triggered=lambda: print("状态栏"), checkable=True, checked=True),
            QAction("自动换行", self, triggered=lambda: print("自动换行"), checkable=True, checked=True),
        ])

        self.menuBar.addMenu(self.fileMenu)
        self.menuBar.addMenu(self.editMenu)
        self.menuBar.addMenu(self.viewMenu)
        self.addExamplesCard(
            "菜单栏",
            self.menuBar
        )

        widget = QWidget()
        widget.setMinimumHeight(328)
        layout = QVBoxLayout(widget)

        self.slidingNavigation: SlidingNavigationBar = SlidingNavigationBar(self)
        self.slidingNavigation.addItem("zy", "主页", FluentIcon.HOME, isSelected=True)
        self.slidingNavigation.addItem("dy", "订阅", FluentIcon.BOOK_SHELF)
        self.slidingNavigation.addItem("ls", "历史", FluentIcon.HISTORY)
        self.slidingNavigation.addItem("xz", "下载", FluentIcon.FOLDER)
        self.slidingNavigation.addItem("wbfdjj", "未播放的剧集", FluentIcon.VIDEO)
        self.slidingNavigation.addItem("zzby", "正在播放", FluentIcon.ALBUM)
        self.slidingNavigation.addItem("yxzx", "游戏中心")
        self.slidingNavigation.addStretch(1)
        self.slidingNavigation.addItem("sz", "", FluentIcon.SETTING)

        self.interfaceLabel: SubtitleLabel = SubtitleLabel("主页", self)
        layout.addWidget(self.slidingNavigation)
        layout.addWidget(self.interfaceLabel, 1, Qt.AlignCenter)

        InfoBadge.attension(9, parent=self.slidingNavigation, target=self.slidingNavigation.item("xz"))
        self.slidingNavigation.currentItemChanged.connect(lambda item: self.interfaceLabel.setText(item.text()))

        view = self.addExamplesCard(
            "滑动顶部导航栏",
            widget,
            1
        ).widget.widgetCard.viewLayout
        view.setSpacing(0)
        view.setContentsMargins(0, 0, 0, 0)

        self.slidingToolNavigation: SlidingToolNavigationBar = SlidingToolNavigationBar(self)
        self.slidingToolNavigation.addItem("zy",  FluentIcon.HOME, isSelected=True)
        self.slidingToolNavigation.addItem("dy",  FluentIcon.BOOK_SHELF)
        self.slidingToolNavigation.addItem("ls", FluentIcon.HISTORY)
        self.slidingToolNavigation.addItem("xz",  FluentIcon.FOLDER)
        self.slidingToolNavigation.addItem("wbfdjj", FluentIcon.VIDEO)
        self.slidingToolNavigation.addItem("zzby",  FluentIcon.ALBUM)
        self.slidingToolNavigation.addStretch(1)
        self.slidingToolNavigation.addItem("sz",  FluentIcon.SETTING)

        InfoBadge.attension(9, parent=self.slidingToolNavigation, target=self.slidingToolNavigation.item("xz"))

        layout = self.addExamplesCard(
            "滑动顶部工具导航栏",
            self.slidingToolNavigation,
            1
        ).widget.widgetCard.viewLayout
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)