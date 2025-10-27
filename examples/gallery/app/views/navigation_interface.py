# coding:utf-8
from PySide6FluentUI import FluentIcon, SlidingNavigationBar, SlidingToolNavigationBar, InfoBadge

from ..widgets.basic_interface import Interface


class NavigationInterface(Interface):
    def __init__(self, parent=None):
        super().__init__("导航", "PySide6FluentUI.components.widgets", parent)
        self.setObjectName("NavigationInterface")
        self.vBoxLayout.addWidget(self.scrollArea)

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

        InfoBadge.attension(9, parent=self.slidingNavigation, target=self.slidingNavigation.item("xz"))

        view = self.addExamplesCard(
            "滑动顶部导航栏",
            self.slidingNavigation,
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

        self.scrollLayout.addStretch(1)