# coding:utf-8
from PySide6.QtCore import Qt
from PySide6FluentUI import FluentIcon, SlidingNavigationBar, SlidingToolNavigationBar, InfoBadge, InfoBadgePosition

from ..widgets.basic_interface import Interface
from ..widgets.widget_item import StandardItem


class NavigationInterface(Interface):
    def __init__(self, parent=None):
        super().__init__("导航", "PySide6FluentUI.components.widgets", parent)
        self.setObjectName("NavigationInterface")
        self.vBoxLayout.addWidget(self.scrollArea)

        self.__initTopNavigation()
        self.__initTopToolNavigation()
        self.scrollLayout.addStretch(1)

    def __initTopNavigation(self):
        self.topSlidingNavItem: StandardItem = StandardItem("滑动顶部导航栏", self)
        self.slidingNav: SlidingNavigationBar = SlidingNavigationBar(self)

        self.slidingNav.addItem("zy", "主页", FluentIcon.HOME, isSelected=True)
        self.slidingNav.addItem("dy", "订阅", FluentIcon.BOOK_SHELF)
        self.slidingNav.addItem("ls", "历史", FluentIcon.HISTORY)
        self.slidingNav.addItem("xz", "下载", FluentIcon.FOLDER)
        self.slidingNav.addItem("wbfdjj", "未播放的剧集", FluentIcon.VIDEO)
        self.slidingNav.addItem("zzby", "正在播放", FluentIcon.ALBUM)
        self.slidingNav.addItem("yxzx", "游戏中心")
        self.slidingNav.addStretch(1)
        self.slidingNav.addItem("sz", "", FluentIcon.SETTING)

        InfoBadge.attension(9, parent=self.slidingNav, target=self.slidingNav.item("xz"))

        self.topSlidingNavItem.card.widgetLayout.setContentsMargins(0, 0, 0, 0)
        self.topSlidingNavItem.card.widgetLayout.setSpacing(0)
        self.topSlidingNavItem.addWidget(self.slidingNav, 1, Qt.AlignmentFlag(0))

        self.scrollLayout.addWidget(self.topSlidingNavItem)

    def __initTopToolNavigation(self):
        self.topSlidingToolNavItem: StandardItem = StandardItem("滑动顶部工具导航栏", self)
        self.slidingToolNav: SlidingToolNavigationBar = SlidingToolNavigationBar(self)

        self.slidingToolNav.addItem("zy",  FluentIcon.HOME, isSelected=True)
        self.slidingToolNav.addItem("dy",  FluentIcon.BOOK_SHELF)
        self.slidingToolNav.addItem("ls", FluentIcon.HISTORY)
        self.slidingToolNav.addItem("xz",  FluentIcon.FOLDER)
        self.slidingToolNav.addItem("wbfdjj", FluentIcon.VIDEO)
        self.slidingToolNav.addItem("zzby",  FluentIcon.ALBUM)
        self.slidingToolNav.addStretch(1)
        self.slidingToolNav.addItem("sz",  FluentIcon.SETTING)

        InfoBadge.attension(9, parent=self.slidingToolNav, target=self.slidingToolNav.item("xz"))

        self.topSlidingToolNavItem.card.widgetLayout.setContentsMargins(0, 0, 0, 0)
        self.topSlidingToolNavItem.card.widgetLayout.setSpacing(0)
        self.topSlidingToolNavItem.addWidget(self.slidingToolNav, 1, Qt.AlignmentFlag(0))

        self.scrollLayout.addWidget(self.topSlidingToolNavItem)